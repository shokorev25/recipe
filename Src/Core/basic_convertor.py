from Src.Core.abstract_convertor import abstract_convertor

class basic_convertor(abstract_convertor):
    """
    Конвертор для простых типов (str, int, float)
    """
    def convert(self, obj) -> dict:
        result = {}
        if obj is None:
            return result

        # Если это простой тип — возвращаем как есть
        if isinstance(obj, (str, int, float, bool)):
            return {"value": obj}

        # Если это объект — проходим по всем свойствам
        for attr in dir(obj):
            if not attr.startswith("_"):
                value = getattr(obj, attr)
                if isinstance(value, (str, int, float, bool)):
                    result[attr] = value
        return result
