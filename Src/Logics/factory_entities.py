from Src.Core.abstract_response import abstract_response
from Src.Logics.response_csv import response_scv
from Src.Logics.response_markdown import response_markdown
from Src.Logics.response_json import response_json
from Src.Logics.response_xml import response_xml
from Src.Core.validator import operation_exception

class factory_entities:
    __match = {
        "csv": response_scv,
        "markdown": response_markdown,
        "json": response_json,
        "xml": response_xml
    }

    def create(self, format:str) -> abstract_response:
        format = format.lower()
        if format not in self.__match:
            raise operation_exception("Формат не верный")
        return self.__match[format]()

    def create_default(self, settings_format:str) -> abstract_response:
        return self.create(settings_format)
