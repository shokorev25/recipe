from Src.Core.abstract_response import abstract_response
from Src.Core.common import common

class response_xml(abstract_response):
    def build(self, format:str, data: list):
        text = super().build(format, data)
        text += "<items>\n"
        for item in data:
            text += "  <item>\n"
            fields = common.get_fields(item)
            for f in fields:
                text += f"    <{f}>{getattr(item, f)}</{f}>\n"
            text += "  </item>\n"
        text += "</items>\n"
        return text
