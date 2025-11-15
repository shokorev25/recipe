import os
import json
from datetime import datetime
from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Models.storage_model import storage_model
from Src.Models.transaction_model import transaction_model
from Src.Dtos.nomenclature_dto import nomenclature_dto
from Src.Dtos.range_dto import range_dto
from Src.Dtos.category_dto import category_dto
from Src.Dtos.storage_dto import storage_dto
from Src.Dtos.transaction_dto import transaction_dto
from Src.Core.validator import validator, argument_exception, operation_exception

class start_service:
    __repo: reposity = reposity()
    __cache = {}
    __full_file_name:str = ""

    def __init__(self):
        self.__repo.initalize()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    @property
    def file_name(self) -> str:
        return self.__full_file_name

    @file_name.setter
    def file_name(self, value:str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")
        try:
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:
                settings = json.load(file_instance)
                return self.convert(settings)
            return False
        except Exception as e:
            raise operation_exception(f"Load error: {e}")

    def __save_item(self, key:str, item, id_:str):
        validator.validate(key, str)
        item.unique_code = id_
        self.__cache.setdefault(id_, item)
        self.__repo.data[key].append(item)

    def __convert_ranges(self, data: dict) -> bool:
        validator.validate(data, dict)
        ranges = data.get('ranges', [])
        if not ranges: return False
        for range_ in ranges:
            dto = range_dto().create(range_)
            item = range_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.range_key(), item, dto.id)
        return True

    def __convert_groups(self, data: dict) -> bool:
        validator.validate(data, dict)
        categories = data.get('categories', [])
        if not categories: return False
        for category in categories:
            dto = category_dto().create(category)
            item = group_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.group_key(), item, dto.id)
        return True

    def __convert_nomenclatures(self, data: dict) -> bool:
        validator.validate(data, dict)
        nomenclatures = data.get('nomenclatures', [])
        if not nomenclatures: return False
        for nomenclature in nomenclatures:
            dto = nomenclature_dto().create(nomenclature)
            item = nomenclature_model.from_dto(dto, self.__cache)
            self.__save_item(reposity.nomenclature_key(), item, dto.id)
        return True

    def __convert_storages(self, data: dict) -> bool:
        validator.validate(data, dict)
        storages = data.get('storages', [])
        for storage in storages:
            dto = storage_dto().create(storage)
            item = storage_model()
            item.name = dto.name
            item.address = dto.address
            self.__save_item(reposity.storage_key(), item, dto.id)
        return True

    def __convert_transactions(self, data: dict) -> bool:
        validator.validate(data, dict)
        transactions = data.get('transactions', [])
        for transaction in transactions:
            dto = transaction_dto().create(transaction)
            nom = self.__cache.get(dto.nomenclature_id)
            st = self.__cache.get(dto.storage_id)
            rn = self.__cache.get(dto.range_id)
            if not all([nom, st, rn]):
                continue
            date = datetime.fromisoformat(dto.date)
            item = transaction_model.create(date, nom, st, dto.quantity, rn)
            self.__save_item(reposity.transaction_key(), item, dto.id)
        return True

    def __convert_receipts(self, data: dict) -> bool:
        validator.validate(data, dict)
        receipts = data.get('receipts', [])
        for rec in receipts:
            name = rec.get('name', "НЕ ИЗВЕСТНО")
            cooking_time = rec.get('cooking_time', "")
            portions = int(rec.get('portions', 0))
            item = receipt_model.create(name, cooking_time, portions)
            item.unique_code = rec.get('id', item.unique_code)
            steps = rec.get('steps', [])
            item.steps = [step.strip() for step in steps if step.strip()]
            composition = rec.get('composition', [])
            for comp in composition:
                nom_id = comp.get('nomenclature_id', "")
                range_id = comp.get('range_id', "")
                value = comp.get('value', 0)
                nom = self.__cache.get(nom_id)
                range_ = self.__cache.get(range_id)
                if nom and range_:
                    comp_item = receipt_item_model.create(nom, range_, value)
                    item.composition.append(comp_item)
            self.__repo.data[reposity.receipt_key()].append(item)
        return True

    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)
        self.__convert_ranges(data)
        self.__convert_groups(data)
        self.__convert_nomenclatures(data)
        self.__convert_storages(data)
        self.__convert_transactions(data)
        self.__convert_receipts(data)
        return True

    @property
    def data(self):
        return self.__repo.data

    def start(self):
        file_path = os.path.join(os.path.dirname(__file__), "settings.json")
        if not os.path.exists(file_path):
            raise operation_exception(f"Файл настроек не найден: {file_path}")
        self.file_name = file_path
        result = self.load()
        if not result:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")