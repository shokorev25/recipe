from Src.Core.validator import validator
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model

class osv_model:
    __nomenclature: nomenclature_model = None
    __unit: range_model = None
    __initial: float = 0.0
    __come: float = 0.0
    __expense: float = 0.0
    __final: float = 0.0

    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: nomenclature_model):
        validator.validate(value, nomenclature_model)
        self.__nomenclature = value

    @property
    def unit(self) -> range_model:
        return self.__unit

    @unit.setter
    def unit(self, value: range_model):
        validator.validate(value, range_model)
        self.__unit = value

    @property
    def initial(self) -> float:
        return self.__initial

    @initial.setter
    def initial(self, value: float):
        validator.validate(value, float)
        self.__initial = value

    @property
    def come(self) -> float:
        return self.__come

    @come.setter
    def come(self, value: float):
        validator.validate(value, float)
        self.__come = value

    @property
    def expense(self) -> float:
        return self.__expense

    @expense.setter
    def expense(self, value: float):
        validator.validate(value, float)
        self.__expense = value

    @property
    def final(self) -> float:
        return self.__final

    @final.setter
    def final(self, value: float):
        validator.validate(value, float)
        self.__final = value


    @staticmethod
    def create(nomenclature: nomenclature_model, unit: range_model,
               initial: float = 0.0, come: float = 0.0,
               expense: float = 0.0, final: float = 0.0):
        item = osv_model()
        item.nomenclature = nomenclature
        item.unit = unit
        item.initial = initial
        item.come = come
        item.expense = expense
        item.final = final
        return item