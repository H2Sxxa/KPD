from typing import Union
from os import listdir
from Remilia.utils.cli import prompts
from .tui import Form,TUI_Builder,DT,RT
from ..yml.app import I18n_Setting,getPath,App_Setting,App_Conf
from ..utils.builder import ChoiceBuilder


class CanBackForm(Form):
    def __init__(self,backto:Form) -> None:
        super().__init__()
        self.backto=backto

class YoN(Form):
    def __init__(self,ques:str=I18n_Setting.global_set.ques) -> None:
        super().__init__()
        self.ques=ques
    async def do_render(self,_:TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=self.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.global_set.as_yes,True),
                ChoiceBuilder.fromdata(I18n_Setting.global_set.as_no,False)
            ]
        ).prompt()
        return ce.data
NRTU=YoN("NOT READY TO USE")
class Intro(Form):
    async def do_render(self,builder:TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.intro.search,NRTU),
                ChoiceBuilder.fromdata(I18n_Setting.intro.setting,Setting(self)),
                ChoiceBuilder.fromdata(I18n_Setting.intro.exit,Exit(self)),
            ]
        ).prompt()
        return await builder.render(ce.data)

class Setting(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.setting.language,Lanugage(self)),
                ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto)
            ]
        ).prompt()
        return await builder.render(ce.data)

class Lanugage(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=ChoiceBuilder.fromlist(listdir(getPath("i18n")))
        ).prompt()
        App_Setting.language._modify("lang",ce.data)
        App_Conf._push(App_Setting)
        return await builder.render(self.backto)

class Exit(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        if await builder.render(YoN(I18n_Setting.global_set.exit)):
            exit()
        else:
            return await builder.render(self.backto)