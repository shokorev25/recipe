from typing import Any, Dict, Set
from datetime import datetime
from Src.Core.abstract_convertor import basic_convertor, datetime_convertor, reference_convertor

class convert_factory:
    def __init__(self):
        self.basic = basic_convertor()
        self.dt = datetime_convertor()
        self.ref = reference_convertor()

    def convert(self, obj: Any) -> Dict[str, Any]:
        visited: Set[int] = set()
        return self._convert_obj(obj, visited)

    def _is_primitive(self, value: Any) -> bool:
        return isinstance(value, (str, int, float, bool))

    def _convert_obj(self, obj: Any, visited: Set[int]) -> Any:
        if obj is None:
            return None

        if self._is_primitive(obj):
            return obj

        if isinstance(obj, datetime):
            return obj.isoformat()

        if isinstance(obj, (list, tuple, set)):
            return [self._convert_obj(item, visited) for item in obj]

        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                result[k] = self._convert_obj(v, visited)
            return result

        oid = id(obj)
        if oid in visited:
            return None
        visited.add(oid)

        try:
            ref_dict = self.ref.convert(obj)
        except Exception:
            ref_dict = {}

        try:
            basic_dict = self.basic.convert(obj)
        except Exception:
            basic_dict = {}

        try:
            dt_dict = self.dt.convert(obj)
        except Exception:
            dt_dict = {}

        result: Dict[str, Any] = {}
        result.update(basic_dict)
        result.update(dt_dict)
        result.update(ref_dict)

        for attr in dir(obj):
            if attr.startswith("_"):
                continue
            try:
                value = getattr(obj, attr)
            except Exception:
                continue
            if callable(value):
                continue
            if attr in result:
                continue
            converted_value = self._convert_obj(value, visited)
            if converted_value is not None:
                result[attr] = converted_value

        visited.remove(oid)
        
        return result