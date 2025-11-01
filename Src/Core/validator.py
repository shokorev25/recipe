
"""
Исключение при проверки аргумента
"""   
class argument_exception(Exception):
    pass     
    
"""
Исключение при выполнении бизнес операции
"""  
class operation_exception(Exception):
    pass    
    

"""
Набор проверок данных
"""
class validator:

    @staticmethod
    def validate( value, type_, len_= None):

        if value is None:
            raise argument_exception("Пустой аргумент")

        if not isinstance(value, type_):
            raise argument_exception(f"Некорректный тип!\nОжидается {type_}. Текущий тип {type(value)}")

        if len(str(value).strip()) == 0:
            raise argument_exception("Пустой аргумент")

        if len_ is not None and len(str(value).strip()) > len_:
            raise argument_exception("Некорректная длина аргумента")

        return True
