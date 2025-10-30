import unittest
from Src.Core.convert_factory import convert_factory
from Src.Models.company_model import company_model

class test_convert_factory(unittest.TestCase):

    def test_convert_company(self):
        obj = company_model()
        obj.name = "FactoryTest"
        obj.inn = 123456789012
        factory = convert_factory()
        result = factory.convert(obj)
        assert result["name"] == "FactoryTest"
        assert result["inn"] == 123456789012
