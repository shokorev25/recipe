import unittest
from Src.start_service import start_service
from Src.reposity import reposity

class TestStartService(unittest.TestCase):
    def test_load(self):
        service = start_service()
        service.file_name = "settings.json"
        result = service.load()
        self.assertTrue(result)
        self.assertGreater(len(service.data[reposity.range_key()]), 0)
        self.assertGreater(len(service.data[reposity.group_key()]), 0)
        self.assertGreater(len(service.data[reposity.nomenclature_key()]), 0)
        self.assertGreater(len(service.data[reposity.storage_key()]), 0)
        self.assertGreater(len(service.data[reposity.transaction_key()]), 0)
        self.assertGreater(len(service.data[reposity.receipt_key()]), 0)