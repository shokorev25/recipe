import abc
from datetime import datetime

class abstract_convertor(abc.ABC):
    """
    Абстрактный класс для конвертации объектов в словари
    """
    @abc.abstractmethod
    def convert(self, obj) -> dict:
        """
        Преобразует объект в словарь вида {имя_поля: значение_поля}
        """
        pass
