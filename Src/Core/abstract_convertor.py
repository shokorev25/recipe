import abc
from datetime import datetime

class abstract_convertor(abc.ABC):
    @abc.abstractmethod
    def convert(self, obj) -> dict:
        """
        Преобразовать объект в словарь.
        Возвращает: { поле: значение }
        """
        pass

class basic_convertor(abstract_convertor):
    def convert(self, obj) -> dict:
        result = {}
        for attr in dir(obj):
            if attr.startswith("_"):
                continue
            value = getattr(obj, attr)
            if isinstance(value, (int, float, str, bool)):
                result[attr] = value
        return result

class datetime_convertor(abstract_convertor):
    def convert(self, obj) -> dict:
        result = {}
        for attr in dir(obj):
            if attr.startswith("_"):
                continue
            value = getattr(obj, attr)
            if isinstance(value, datetime):
                result[attr] = value.isoformat()
        return result

from Src.Core.entity_model import entity_model
class reference_convertor(abstract_convertor):
    def convert(self, obj) -> dict:
        result = {}
        for attr in dir(obj):
            if attr.startswith("_"):
                continue
            value = getattr(obj, attr)
            if isinstance(value, entity_model):
                result[attr] = getattr(value, "name", str(value))
        return result
