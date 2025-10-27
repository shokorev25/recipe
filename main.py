import connexion
from flask import request, jsonify
from Src.start_service import start_service
from Src.reposity import reposity
from Src.Logics.factory_entities import factory_entities
from Src.Core.convert_factory import convert_factory

app = connexion.FlaskApp(__name__)
service = start_service()
service.start()  
factory = factory_entities()

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
        "group": reposity.group_key()
    }

    if entity not in key_map:
        return jsonify({"error": "Unknown entity"}), 404

    data_list = service.data[key_map[entity]]

    try:
        logic = factory.create(fmt)
        text = logic.build(fmt, data_list)
        return text, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/receipts", methods=['GET'])
def get_receipts():
    receipts = service.data[reposity.receipt_key()]
    result = [factory.convert(r) for r in receipts]
    return jsonify(result)

@app.route("/api/receipt/<code>", methods=['GET'])
def get_receipt(code):
    receipts = service.data[reposity.receipt_key()]
    receipt = next((r for r in receipts if r.unique_code == code), None)
    if not receipt:
        return jsonify({"error":"Receipt not found"}), 404
    return jsonify(factory.convert(receipt))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
