from Src.Core.abstract_response import abstract_response
import json

class response_json(abstract_response):
    def build(self, format:str, data: list):
        text = super().build(format, data)
        result = []
        for item in data:
            fields = [f for f in dir(item.__class__) if isinstance(getattr(item.__class__, f), property)]
            result.append({f: getattr(item, f) for f in fields})
        return json.dumps(result, ensure_ascii=False, indent=2)
