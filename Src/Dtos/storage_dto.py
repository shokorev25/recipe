from Src.Core.abstract_dto import abstact_dto

class storage_dto(abstact_dto):
    __address: str = ""

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, value):
        self.__address = value