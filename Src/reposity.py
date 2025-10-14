
"""
Репозиторий данных
"""
class reposity:
    __data = {}

    @property
    def data(self):
        return self.__data

    """
    Ключи для хранения данных
    """
    @staticmethod
    def range_key(): return "range_model"

    @staticmethod
    def group_key(): return "group_model"

    @staticmethod
    def nomenclature_key(): return "nomenclature_model"

    @staticmethod
    def receipt_key(): return "receipt_model"

    """
    Универсальное получение ключей для модели
    """
    @staticmethod
    def get_key_for_model(model_type: type) -> str:
        mapping = {
            "range_model": reposity.range_key(),
            "group_model": reposity.group_key(),
            "nomenclature_model": reposity.nomenclature_key(),
            "receipt_model": reposity.receipt_key(),
        }
        name = model_type.__name__
        return mapping.get(name, name)

    """
    Инициализация
    """
    def initalize(self):
        for key in [
            reposity.range_key(),
            reposity.group_key(),
            reposity.nomenclature_key(),
            reposity.receipt_key()
        ]:
            self.__data[key] = []
