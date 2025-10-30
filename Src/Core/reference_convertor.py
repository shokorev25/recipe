from Src.Core.abstract_convertor import abstract_convertor

class reference_convertor(abstract_convertor):
 
    def convert(self, obj) -> dict:
        if obj is None:
            return {}

        result = {}

        name = getattr(obj, "name", None)
        code = getattr(obj, "unique_code", None) or getattr(obj, "code", None)
        if name is not None:
            result["name"] = name
        if code is not None:
            result["code"] = code

        return result
