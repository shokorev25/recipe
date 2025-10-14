
from typing import List, Optional

class RangeDTO:
    def __init__(self, id:str, name:str, value:int=1, base_id:Optional[str]=None):
        self.id = id
        self.name = name
        self.value = value
        self.base_id = base_id

class GroupDTO:
    def __init__(self, id:str, name:str):
        self.id = id
        self.name = name

class NomenclatureDTO:
    def __init__(self, id:str, name:str, range_id:str, category_id:str):
        self.id = id
        self.name = name
        self.range_id = range_id
        self.category_id = category_id

class CompositionDTO:
    def __init__(self, nomenclature_id:str, range_id:str, value:int):
        self.nomenclature_id = nomenclature_id
        self.range_id = range_id
        self.value = value

class ReceiptDTO:
    def __init__(self, name:str, cooking_time:str, portions:int,
                 ranges:List[RangeDTO], categories:List[GroupDTO],
                 nomenclatures:List[NomenclatureDTO], composition:List[CompositionDTO], steps:List[str]):
        self.name = name
        self.cooking_time = cooking_time
        self.portions = portions
        self.ranges = ranges
        self.categories = categories
        self.nomenclatures = nomenclatures
        self.composition = composition
        self.steps = steps

class CompanyDTO:
    def __init__(self, name:str, inn:int):
        self.name = name
        self.inn = inn

class SettingsDTO:
    def __init__(self, company:CompanyDTO, default_receipt:ReceiptDTO):
        self.company = company
        self.default_receipt = default_receipt
