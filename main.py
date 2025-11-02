import json
import connexion
from flask import request, jsonify
from datetime import datetime
from collections import defaultdict
from Src.start_service import start_service
from Src.settings_manager import settings_manager
from Src.reposity import reposity
from Src.Logics.factory_entities import factory_entities
from Src.Core.convert_factory import convert_factory
from Src.Models.osv_model import osv_model
from Src.Core.validator import operation_exception

app = connexion.FlaskApp(__name__)

settings_m = settings_manager()
settings_m.file_name = "settings.json"
settings_m.load()

service = start_service()
service.file_name = "settings.json"
if settings_m.settings.first_start:
    service.load()

factory = factory_entities()
converter = convert_factory()

@app.route("/api/accessibility", methods=['GET'])
def accessibility():
    return "SUCCESS"

@app.route("/api/data/<entity>", methods=['GET'])
def get_data(entity):
    fmt = request.args.get('format', 'csv').lower()
    key_map = {
        "nomenclature": reposity.nomenclature_key(),
        "range": reposity.range_key(),
        "receipt": reposity.receipt_key(),
        "group": reposity.group_key(),
        "storage": reposity.storage_key(),
        "transaction": reposity.transaction_key()
    }
    if entity not in key_map:
        return jsonify({"error": "Unknown entity"}), 404
    data_list = service.data[key_map[entity]]
    try:
        if fmt == "json":
            converted = [converter.convert(item) for item in data_list]
            return jsonify(converted)
        logic = factory.create(fmt)
        text = logic.build(fmt, data_list)
        return text, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/receipts", methods=['GET'])
def get_receipts():
    receipts = service.data[reposity.receipt_key()]
    result = [converter.convert(r) for r in receipts]
    return jsonify(result), 200

@app.route("/api/receipt/<code>", methods=['GET'])
def get_receipt(code):
    receipts = service.data[reposity.receipt_key()]
    receipt = next((r for r in receipts if r.unique_code == code), None)
    if not receipt:
        return jsonify({"error": "Receipt not found"}), 404
    result = converter.convert(receipt)
    return jsonify(result), 200

@app.route("/api/save", methods=['POST'])
def save_data():
    try:
        settings_dict = {
            "company": converter.convert(settings_m.settings.company),
            "response_format": settings_m.settings.response_format,
            "first_start": settings_m.settings.first_start,
            "categories": [converter.convert(g) for g in service.data[reposity.group_key()]],
            "ranges": [converter.convert(r) for r in service.data[reposity.range_key()]],
            "nomenclatures": [converter.convert(n) for n in service.data[reposity.nomenclature_key()]],
            "storages": [converter.convert(s) for s in service.data[reposity.storage_key()]],
            "transactions": [
                {
                    "id": t.unique_code,
                    "date": t.date.isoformat(),
                    "nomenclature_id": t.nomenclature.unique_code,
                    "storage_id": t.storage.unique_code,
                    "quantity": t.quantity,
                    "range_id": t.range.unique_code
                } for t in service.data[reposity.transaction_key()]
            ],
            "receipts": [
                {
                    "id": r.unique_code,
                    "name": r.name,
                    "portions": r.portions,
                    "cooking_time": r.cooking_time,
                    "steps": r.steps,
                    "composition": [
                        {
                            "nomenclature_id": i.nomenclature.unique_code,
                            "range_id": i.range.unique_code,
                            "value": i.value
                        } for i in r.composition
                    ]
                } for r in service.data[reposity.receipt_key()]
            ]
        }
        with open(service.file_name, 'w', encoding='utf-8') as f:
            json.dump(settings_dict, f, ensure_ascii=False, indent=2)
        return "SUCCESS", 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/report/osv", methods=['GET'])
def get_osv():
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        storage_code = request.args.get('storage')
        fmt = request.args.get('format', settings_m.settings.response_format)
        if not all([start_date_str, end_date_str, storage_code]):
            return jsonify({"error": "Missing parameters"}), 400
        start_date = datetime.fromisoformat(start_date_str)
        end_date = datetime.fromisoformat(end_date_str)
        storage = next((s for s in service.data[reposity.storage_key()] if s.unique_code == storage_code), None)
        if not storage:
            return jsonify({"error": "Storage not found"}), 404
        transactions = service.data[reposity.transaction_key()]
        nomenclatures = service.data[reposity.nomenclature_key()]
        initial = defaultdict(float)
        come = defaultdict(float)
        expense = defaultdict(float)
        for trans in transactions:
            if trans.storage != storage:
                continue
            nom = trans.nomenclature
            target_range = nom.range
            conv_factor = trans.range.get_factor_to_base() / target_range.get_factor_to_base()
            q_base = trans.quantity * conv_factor
            if trans.date < start_date:
                initial[nom.unique_code] += q_base
            elif start_date <= trans.date <= end_date:
                if q_base > 0:
                    come[nom.unique_code] += q_base
                else:
                    expense[nom.unique_code] += abs(q_base)
        osv_list = []
        for nom in nomenclatures:
            code = nom.unique_code
            init = initial[code]
            c = come[code]
            e = expense[code]
            fin = init + c - e
            row = osv_model()
            row.nomenclature = nom.name
            row.unit = nom.range.name
            row.initial = init
            row.come = c
            row.expense = e
            row.final = fin
            osv_list.append(row)
        if fmt == "json":
            converted = [converter.convert(item) for item in osv_list]
            return jsonify(converted)
        logic = factory.create(fmt)
        text = logic.build(fmt, osv_list)
        return text, 200
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400
    except operation_exception as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)