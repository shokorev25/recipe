import unittest
from datetime import datetime
from Src.Models.osv_model import osv_model
from Src.Models.transaction_model import transaction_model
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.range_model import range_model
from Src.Models.group_model import group_model
from Src.Models.storage_model import storage_model
from Src.reposity import reposity
from Src.start_service import start_service

class TestOSV(unittest.TestCase):
    def setUp(self):
        self.service = start_service()
        self.service.file_name = "settings.json"
        self.service.load()

    def test_osv_calculation(self):
        start_date = datetime.fromisoformat("2025-10-01")
        end_date = datetime.fromisoformat("2025-10-31")
        storage = self.service.data[reposity.storage_key()][0]
        transactions = self.service.data[reposity.transaction_key()]
        nomenclatures = self.service.data[reposity.nomenclature_key()]

        from collections import defaultdict
        initial = defaultdict(float)
        come = defaultdict(float)
        expense = defaultdict(float)

        for trans in transactions:
            if trans.storage != storage:
                continue
            nom = trans.nomenclature
            target_range = nom.range
            conv_factor = trans.range.get_factor_to_base() / target_range.get_factor_to_base()
            q_base = trans.quantity * conv_factor
            if trans.date < start_date:
                initial[nom.unique_code] += q_base
            elif start_date <= trans.date <= end_date:
                if q_base > 0:
                    come[nom.unique_code] += q_base
                else:
                    expense[nom.unique_code] += abs(q_base)

        for nom in nomenclatures:
            code = nom.unique_code
            init = initial[code]
            c = come[code]
            e = expense[code]
            fin = init + c - e
            # Assert for known data
            if nom.name == "Пшеничная мука":
                self.assertEqual(init, 5.0)  # 5000g / 1000 = 5kg since range kg
                self.assertEqual(c, 0.0)
                self.assertEqual(e, 1.0)  # 1000g =1kg
                self.assertEqual(fin, 4.0)
            # Add more assertions for other noms