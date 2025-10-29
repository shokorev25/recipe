import unittest
from datetime import datetime
from Src.Core.basic_convertor import basic_convertor
from Src.Core.datetime_convertor import datetime_convertor
from Src.Core.reference_convertor import reference_convertor
from Src.Core.convert_factory import convert_factory
from Src.Models.company_model import company_model

class Dummy:
    def __init__(self):
        self.name = "Тест"
        self.value = 42
        self.created = datetime(2025, 1, 1, 12, 0, 0)

class TestConvertors(unittest.TestCase):

    def test_basic_convertor(self):
        dummy = Dummy()
        conv = basic_convertor()
        result = conv.convert(dummy)
        self.assertIn("name", result)
        self.assertEqual(result["value"], 42)

    def test_datetime_convertor(self):
        dummy = Dummy()
        conv = datetime_convertor()
        result = conv.convert(dummy)
        self.assertIn("created", result)
        self.assertTrue(result["created"].startswith("2025-01-01T"))

    def test_reference_convertor(self):
        company = company_model()
        company.name = "ООО Рога и Копыта"
        company.unique_code = "abc123"
        conv = reference_convertor()
        result = conv.convert(company)
        self.assertEqual(result["name"], "ООО Рога и Копыта")
        self.assertEqual(result["code"], "abc123")

    def test_convert_factory_basic(self):
        dummy = Dummy()
        factory = convert_factory()
        result = factory.convert(dummy)
        self.assertIn("name", result)
        self.assertIn("created", result)

    def test_convert_factory_reference(self):
        company = company_model()
        company.name = "TestOrg"
        company.unique_code = "xyz"
        factory = convert_factory()
        result = factory.convert(company)
        self.assertEqual(result["name"], "TestOrg")
        self.assertEqual(result["code"], "xyz")

if __name__ == '__main__':
    unittest.main()
