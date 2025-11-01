from Src.Core.abstract_dto import abstact_dto

class transaction_dto(abstact_dto):
    __date: str = ""
    __nomenclature_id: str = ""
    __storage_id: str = ""
    __quantity: float = 0.0
    __range_id: str = ""

    @property
    def date(self) -> str:
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    @property
    def nomenclature_id(self) -> str:
        return self.__nomenclature_id

    @nomenclature_id.setter
    def nomenclature_id(self, value):
        self.__nomenclature_id = value

    @property
    def storage_id(self) -> str:
        return self.__storage_id

    @storage_id.setter
    def storage_id(self, value):
        self.__storage_id = value

    @property
    def quantity(self) -> float:
        return self.__quantity

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value

    @property
    def range_id(self) -> str:
        return self.__range_id

    @range_id.setter
    def range_id(self, value):
        self.__range_id = value