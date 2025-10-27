import unittest, os
from Src.start_service import start_service
from Src.Logics.factory_entities import factory_entities
from Src.reposity import reposity

class test_export_formats(unittest.TestCase):
    def test_generate_all_formats(self):
        start = start_service()
        start.start()
        data = start.data[reposity.range_key()]
        factory = factory_entities()

        for fmt in ["csv", "markdown", "json", "xml"]:
            logic_class = factory.create(fmt)
            instance = eval(logic_class)()
            result = instance.build(fmt, data)
            file_name = f"export_{fmt}.txt"
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(result)
            assert os.path.exists(file_name)
            assert len(result) > 0

if __name__ == '__main__':
    unittest.main()
