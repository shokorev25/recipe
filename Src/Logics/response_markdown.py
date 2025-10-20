from Src.Core.abstract_response import abstract_response
from Src.Core.common import common

class response_markdown(abstract_response):
    def build(self, format:str, data: list):
        text = super().build(format, data)
        fields = common.get_fields(data[0])
        text += "| " + " | ".join(fields) + " |\n"
        text += "| " + " | ".join(["---"]*len(fields)) + " |\n"
        for item in data:
            row = [str(getattr(item, f)) for f in fields]
            text += "| " + " | ".join(row) + " |\n"
        return text
