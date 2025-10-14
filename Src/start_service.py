from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_model import receipt_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Models.dto import *
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json

class start_service:
    __repo: reposity = reposity()
    __default_receipt: receipt_model = None
    __default_receipt_items = {}
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
            with open(self.__full_file_name, 'r') as file_instance:
                settings = json.load(file_instance)
                return self.convert(settings)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False

    def __convert_dto(self, dto_list, create_func, ref_keys:dict = None):
        for dto in dto_list:
            kwargs = {}
            if ref_keys:
                for prop, ref_id in ref_keys.items():
                    kwargs[prop] = self.__default_receipt_items.get(getattr(dto, ref_id))
            item = create_func(dto.name, **kwargs)
            if hasattr(dto, 'id') and dto.id:
                item.unique_code = dto.id
                self.__default_receipt_items[dto.id] = item
            self.__repo.data[reposity.get_key_for_model(type(item))].append(item)

    def convert(self, data: dict) -> bool:
        validator.validate(data, dict)

        # Создаём DTO объекты
        company_dto = CompanyDTO(**data['company'])
        receipt_data = data['default_receipt']

        ranges_dto = [RangeDTO(**r) for r in receipt_data.get('ranges',[])]
        groups_dto = [GroupDTO(**c) for c in receipt_data.get('categories',[])]
        nomenclature_dto = [NomenclatureDTO(**n) for n in receipt_data.get('nomenclatures',[])]
        composition_dto = [CompositionDTO(**c) for c in receipt_data.get('composition',[])]
        steps = receipt_data.get('steps', [])

        receipt_dto = ReceiptDTO(
            name=receipt_data.get('name', 'НЕ ИЗВЕСТНО'),
            cooking_time=receipt_data.get('cooking_time',''),
            portions=int(receipt_data.get('portions',0)),
            ranges=ranges_dto,
            categories=groups_dto,
            nomenclatures=nomenclature_dto,
            composition=composition_dto,
            steps=steps
        )

        # 1. Создаём рецепт
        self.__default_receipt = receipt_model.create(receipt_dto.name, receipt_dto.cooking_time, receipt_dto.portions)

        # 2. Шаги
        for step in receipt_dto.steps:
            if step.strip() != "":
                self.__default_receipt.steps.append(step)

        # 3. Создаём модели через универсальный конвертер
        # ranges
        for r in receipt_dto.ranges:
            base = self.__default_receipt_items.get(r.base_id) if r.base_id else None
            item = range_model.create(r.name, r.value, base)
            item.unique_code = r.id
            self.__default_receipt_items[r.id] = item
            self.__repo.data[reposity.get_key_for_model(type(item))].append(item)

        # groups
        for g in receipt_dto.categories:
            item = group_model.create(g.name)
            item.unique_code = g.id
            self.__default_receipt_items[g.id] = item
            self.__repo.data[reposity.get_key_for_model(type(item))].append(item)

        # nomenclature
        for n in receipt_dto.nomenclatures:
            rng = self.__default_receipt_items.get(n.range_id)
            grp = self.__default_receipt_items.get(n.category_id)
            item = nomenclature_model.create(n.name, grp, rng)
            item.unique_code = n.id
            self.__default_receipt_items[n.id] = item
            self.__repo.data[reposity.get_key_for_model(type(item))].append(item)

        # composition
        for c in receipt_dto.composition:
            nom = self.__default_receipt_items.get(c.nomenclature_id)
            rng = self.__default_receipt_items.get(c.range_id)
            item = receipt_item_model.create(nom, rng, c.value)
            self.__default_receipt.composition.append(item)

        # сохраняем рецепт
        self.__repo.data[reposity.get_key_for_model(type(self.__default_receipt))].append(self.__default_receipt)
        return True

    @property
    def data(self):
        return self.__repo.data   

    def start(self):
        self.file_name = "settings.json"
        result = self.load()
        if not result:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")
