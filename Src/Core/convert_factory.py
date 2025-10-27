from Src.Core.abstract_convertor import basic_convertor, datetime_convertor, reference_convertor
from datetime import datetime
from Src.Core.entity_model import entity_model

class convert_factory:
    def __init__(self):
        self.basic = basic_convertor()
        self.datetime = datetime_convertor()
        self.reference = reference_convertor()

    def convert(self, obj) -> dict:
        result = {}
        result.update(self.basic.convert(obj))
        result.update(self.datetime.convert(obj))
        result.update(self.reference.convert(obj))
        return result
