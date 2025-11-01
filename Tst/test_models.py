import unittest
from Src.Models.range_model import range_model
from Src.Models.transaction_model import transaction_model
from datetime import datetime
from Src.Models.nomenclature_model import nomenclature_model
from Src.Models.group_model import group_model
from Src.Models.storage_model import storage_model

class TestModels(unittest.TestCase):
    def test_range_factor(self):
        gram = range_model()
        gram.name = "Грамм"
        gram.value = 1
        gram.base = None

        kg = range_model()
        kg.name = "Киллограмм"
        kg.value = 1000
        kg.base = gram

        self.assertEqual(gram.get_factor_to_base(), 1)
        self.assertEqual(kg.get_factor_to_base(), 1000)

    def test_transaction_create(self):
        group = group_model()
        group.name = "Test Group"

        range_ = range_model()
        range_.name = "Test Range"
        range_.value = 1

        nom = nomenclature_model()
        nom.name = "Test Nom"
        nom.group = group
        nom.range = range_

        storage = storage_model()
        storage.name = "Test Storage"
        storage.address = "Test Address"

        trans = transaction_model.create(
            datetime.now(),
            nom,
            storage,
            10.0,
            range_
        )
        self.assertEqual(trans.quantity, 10.0)