from Src.Core.abstract_model import abstact_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model

# Модель элемента рецепта
class receipt_item_model(abstact_model):
    __nomenclature:nomenclature_model = None
    __range:range_model = None
    __value:int = 0

    # Фабричный метод
    @staticmethod
    def create(nomenclature:nomenclature_model, range:range_model,  value:int):
        item = receipt_item_model()
        item.nomenclature = nomenclature
        item.range = range
        item.value = value
        return item

    # Свойства
    @property
    def nomenclature(self) -> nomenclature_model:
        return self.__nomenclature
    
    @nomenclature.setter
    def nomenclature(self, value:nomenclature_model):
        self.__nomenclature = value

    @property
    def range(self) -> range_model:
        return self.__range
    
    @range.setter
    def range(self, value:range_model):
        self.__range = value

    @property
    def value(self) -> int:
        return self.__value
    
    @value.setter
    def value(self, val:int):
        self.__value = val
