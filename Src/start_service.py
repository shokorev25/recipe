from Src.reposity import reposity
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.receipt_item_model import receipt_item_model
from Src.Models.receipt_model import receipt_model
from Src.Core.validator import validator, argument_exception, operation_exception
import os
import json

class start_service:
    __repo: reposity = reposity()
    __default_receipt: receipt_model
    __default_receipt_items = {}
    __full_file_name: str = ""

    def __init__(self):
        self.__repo.initalize()

    # Singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(start_service, cls).__new__(cls)
        return cls.instance

    @property
    def file_name(self) -> str:
        return self.__full_file_name

    @file_name.setter
    def file_name(self, value: str):
        validator.validate(value, str)
        full_file_name = os.path.abspath(value)
        if os.path.exists(full_file_name):
            self.__full_file_name = full_file_name.strip()
        else:
            raise argument_exception(f'Не найден файл настроек {full_file_name}')

    """
    Загрузка JSON данных
    """
    def load(self) -> bool:
        if self.__full_file_name == "":
            raise operation_exception("Не найден файл настроек!")

        try:
            with open(self.__full_file_name, 'r', encoding='utf-8') as file_instance:
                settings = json.load(file_instance)
                if "default_receipt" in settings:
                    return self.convert(settings["default_receipt"])
            return False
        except Exception as ex:
            print(f"[Ошибка] Загрузка настроек: {ex}")
            return False

    """
    Универсальный метод загрузки коллекций
    """
    def __convert_items(self, data: list, model_class, create_func, **kwargs):
        if not isinstance(data, list):
            return False

        for record in data:
            try:
                name = record.get("name", "")
                id_ = record.get("id", "")
                if not id_.strip():
                    continue

                obj_args = {k: record.get(v) for k, v in kwargs.items()}
                item = create_func(name, **{k: self.__default_receipt_items.get(v) for k, v in obj_args.items() if v})
                item.unique_code = id_
                self.__default_receipt_items[id_] = item
                self.__repo.data[reposity.get_key_for_model(model_class)].append(item)
            except Exception as ex:
                print(f"[Ошибка] Конвертация {model_class.__name__}: {ex}")
                return False
        return True

    """
    Универсальная функция конверсии JSON → модели
    """
    def convert(self, data: dict) -> bool:
        try:
            validator.validate(data, dict)

            # Создание рецепта
            cooking_time = data.get("cooking_time", "")
            portions = int(data.get("portions", 0))
            name = data.get("name", "НЕИЗВЕСТНО")
            self.__default_receipt = receipt_model.create(name, cooking_time, portions)

            for step in data.get("steps", []):
                if step.strip():
                    self.__default_receipt.steps.append(step)

            self.__convert_ranges(data)
            self.__convert_groups(data)
            self.__convert_nomenclatures(data)

            for comp in data.get("composition", []):
                try:
                    nomenclature_id = comp.get("nomenclature_id", "")
                    range_id = comp.get("range_id", "")
                    value = int(comp.get("value", 0))

                    nomenclature = self.__default_receipt_items.get(nomenclature_id)
                    range_obj = self.__default_receipt_items.get(range_id)
                    if nomenclature and range_obj:
                        item = receipt_item_model.create(nomenclature, range_obj, value)
                        self.__default_receipt.composition.append(item)
                except Exception as ex:
                    print(f"[Ошибка] Состав рецепта: {ex}")
                    continue

            self.__repo.data[reposity.receipt_key()].append(self.__default_receipt)
            return True
        except Exception as ex:
            print(f"[Ошибка convert]: {ex}")
            return False

    """
    Преобразование отдельных сущностей
    """
    def __convert_ranges(self, data: dict) -> bool:
        try:
            for record in data.get("ranges", []):
                name = record.get("name", "")
                base_id = record.get("base_id")
                value = int(record.get("value", 1))
                id_ = record.get("id", "")
                if not id_.strip():
                    continue
                base = self.__default_receipt_items.get(base_id) if base_id else None
                item = range_model.create(name, value, base)
                item.unique_code = id_
                self.__default_receipt_items[id_] = item
                self.__repo.data[reposity.range_key()].append(item)
            return True
        except Exception as ex:
            print(f"[Ошибка диапазонов]: {ex}")
            return False

    def __convert_groups(self, data: dict) -> bool:
        try:
            for record in data.get("categories", []):
                name = record.get("name", "")
                id_ = record.get("id", "")
                if not id_.strip():
                    continue
                item = group_model.create(name)
                item.unique_code = id_
                self.__default_receipt_items[id_] = item
                self.__repo.data[reposity.group_key()].append(item)
            return True
        except Exception as ex:
            print(f"[Ошибка групп]: {ex}")
            return False

    def __convert_nomenclatures(self, data: dict) -> bool:
        try:
            for record in data.get("nomenclatures", []):
                name = record.get("name", "")
                id_ = record.get("id", "")
                range_id = record.get("range_id", "")
                category_id = record.get("category_id", "")

                if not id_.strip():
                    continue

                range_obj = self.__default_receipt_items.get(range_id)
                category_obj = self.__default_receipt_items.get(category_id)
                item = nomenclature_model.create(name, category_obj, range_obj)
                item.unique_code = id_
                self.__default_receipt_items[id_] = item
                self.__repo.data[reposity.nomenclature_key()].append(item)
            return True
        except Exception as ex:
            print(f"[Ошибка номенклатуры]: {ex}")
            return False

    """
    Стартовые данные
    """
    @property
    def data(self):
        return self.__repo.data

   
    def start(self):
        self.file_name = "settings.json"
        result = self.load()
        if not result:
            raise operation_exception("Невозможно сформировать стартовый набор данных!")
        