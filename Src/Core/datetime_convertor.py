from Src.Core.abstract_convertor import abstract_convertor
from datetime import datetime

class datetime_convertor(abstract_convertor):
    """
    Конвертор для объектов с полями типа datetime
    """
    def convert(self, obj) -> dict:
        result = {}
        if obj is None:
            return result

        if isinstance(obj, datetime):
            return {"value": obj.isoformat()}

        for attr in dir(obj):
            if not attr.startswith("_"):
                value = getattr(obj, attr)
                if isinstance(value, datetime):
                    result[attr] = value.isoformat()
        return result
