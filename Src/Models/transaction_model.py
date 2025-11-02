from datetime import datetime
from Src.Core.abstract_model import abstact_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.storage_model import storage_model
from Src.Models.range_model import range_model
from Src.Core.validator import validator

class transaction_model(abstact_model):
    __date: datetime = None
    __nomenclature: nomenclature_model = None
    __storage: storage_model = None
    __quantity: float = 0.0
    __range: range_model = None

    @property
    def date(self) -> datetime:
        return self.__date

    @date.setter
    def date(self, value: datetime):
        validator.validate(value, datetime)
        self.__date = value

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def storage(self) -> storage_model:
        return self.__storage

    @storage.setter
    def storage(self, value: storage_model):
        validator.validate(value, storage_model)
        self.__storage = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        if isinstance(value, int):
            value = float(value)
        elif not isinstance(value, float):
            raise ValueError("Quantity must be int or float")
        validator.validate(value, float)
        self.__quantity = value

    @property
    def range(self) -> range_model:
        return self.__range

    @range.setter
    def range(self, value: range_model):
        validator.validate(value, range_model)
        self.__range = value

    @staticmethod
    def create(date: datetime, nomenclature: nomenclature_model, storage: storage_model, quantity: float, range: range_model):
        item = transaction_model()
        item.date = date
        item.nomenclature = nomenclature
        item.storage = storage
        item.quantity = quantity
        item.range = range
        return item