from Src.Core.validator import validator

class osv_model:
    __nomenclature: str = ""
    __unit: str = ""
    __initial: float = 0.0
    __come: float = 0.0
    __expense: float = 0.0
    __final: float = 0.0

    @property
    def nomenclature(self) -> str:
        return self.__nomenclature

    @nomenclature.setter
    def nomenclature(self, value: str):
        validator.validate(value, str)
        self.__nomenclature = value.strip()

    @property
    def unit(self) -> str:
        return self.__unit

    @unit.setter
    def unit(self, value: str):
        validator.validate(value, str)
        self.__unit = value.strip()

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