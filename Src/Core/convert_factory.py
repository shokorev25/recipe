from datetime import datetime, date
from typing import Any
from Src.Core.basic_convertor import basic_convertor
from Src.Core.datetime_convertor import datetime_convertor
from Src.Core.reference_convertor import reference_convertor
from Src.Core.abstract_model import abstact_model
from Src.Core.common import common

class convert_factory:

    def __init__(self):
        self.basic = basic_convertor()
        self.dt = datetime_convertor()
        self.ref = reference_convertor()

    def convert(self, obj: Any):
        seen = set()
        return self._convert(obj, seen)

    def _primitive(self, obj: Any):
        if isinstance(obj, (str, int, float, bool)):
            return obj
        return None

    def _is_datetime(self, obj: Any) -> bool:
        return isinstance(obj, (datetime, date))

    def _is_iterable(self, obj: Any) -> bool:
        return isinstance(obj, (list, tuple, set))

    def _convert(self, obj: Any, seen: set):
        if obj is None:
            return None

        prim = self._primitive(obj)
        if prim is not None:
            return prim

        if self._is_datetime(obj):
            try:
                return obj.isoformat()
            except Exception:
                return str(obj)

        try:
            obj_id = id(obj)
        except Exception:
            obj_id = None

        if obj_id is not None:
            if obj_id in seen:
                return "<recursion>"
            seen.add(obj_id)

        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                if isinstance(k, (str, int, float, bool)):
                    key = k
                else:
                    key = str(k)
                result[key] = self._convert(v, seen)
            if obj_id is not None:
                seen.discard(obj_id)
            return result

        if self._is_iterable(obj):
            result = [self._convert(item, seen) for item in obj]
            if obj_id is not None:
                seen.discard(obj_id)
            return result

        if isinstance(obj, abstact_model):
            base = self.ref.convert(obj)
            try:
                fields = common.get_fields(obj)
            except Exception:
                fields = []

            for f in fields:
                try:
                    value = getattr(obj, f)
                    base[f] = self._convert(value, seen)
                except Exception:
                    base[f] = None

            if obj_id is not None:
                seen.discard(obj_id)
            return base

        try:
            fields = common.get_fields(obj)
        except Exception:
            fields = []

        if fields:
            result = {}
            for f in fields:
                try:
                    value = getattr(obj, f)
                except Exception:
                    value = None
                result[f] = self._convert(value, seen)
            if obj_id is not None:
                seen.discard(obj_id)
            return result

        try:
            text = str(obj)
            if obj_id is not None:
                seen.discard(obj_id)
            return text
        except Exception:
            if obj_id is not None:
                seen.discard(obj_id)
            return None
