from typing import List
from Remilia.utils.cli.prompts import Choice


class ChoiceBuilder:
    @staticmethod
    def fromdata(name:str,data) -> Choice:
        return Choice(name,data)
    
    @staticmethod
    def fromlist(target:list,name_warp=lambda _:_,data_warp=lambda _:_) -> List[Choice]:
        return [Choice(name_warp(name),data_warp(name)) for name in target]