from typing import List
from Remilia.utils.cli import prompts


class ChoiceBuilder:
    @staticmethod
    def fromdata(name:str,data) -> prompts.Choice:
        return prompts.Choice(name,data)
    
    @staticmethod
    def fromlist(target:list,name_warp=lambda _:_,data_warp=lambda _:_) -> List[prompts.Choice]:
        return [prompts.Choice(name_warp(name),data_warp(name)) for name in target]