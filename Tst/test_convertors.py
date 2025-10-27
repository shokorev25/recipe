import unittest
from datetime import datetime
from Src.Core.abstract_convertor import basic_convertor, datetime_convertor, reference_convertor
from Src.Models.company_model import company_model

class test_convertors(unittest.TestCase):

    def test_basic_convertor(self):
        obj = company_model()
        obj.name = "TestCompany"
        obj.inn = 123456789012
        conv = basic_convertor()
        result = conv.convert(obj)
        assert "name" in result
        assert result["name"] == "TestCompany"
        assert "inn" in result
        assert result["inn"] == 123456789012

    def test_datetime_convertor(self):
        class obj:
            dt = datetime(2025, 10, 20, 12, 30)
        conv = datetime_convertor()
        result = conv.convert(obj())
        assert "dt" in result
        assert result["dt"] == "2025-10-20T12:30:00"

    def test_reference_convertor(self):
        obj = company_model()
        obj.name = "RefCompany"
        conv = reference_convertor()
        result = conv.convert(obj)
        assert "name" in result
        assert result["name"] == "RefCompany"
