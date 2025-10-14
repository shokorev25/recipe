
"""
Репозиторий данных
"""
class reposity:
    __data = {}

    @property
    def data(self):
        return self.__data
    
    """
    Универсальный ключ для модели
    """
    @staticmethod
    def get_key_for_model(model_type: type) -> str:
        return model_type.__name__.lower()

    # Инициализация
    def initalize(self):
        self.__data[reposity.get_key_for_model('range_model')] = []
        self.__data[reposity.get_key_for_model('group_model')] = []
        self.__data[reposity.get_key_for_model('nomenclature_model')] = []
        self.__data[reposity.get_key_for_model('receipt_model')] = []
