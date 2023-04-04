from .tui import Form,prompts
from ..yml.app import I18n_Setting
from ..utils.builder import ChoiceBuilder


class YoN(Form):
    async def do_render(self):
        return await prompts.ListPrompt(
            question=I18n_Setting.intro.ques,
            choices=[
                ChoiceBuilder.fromdata("yes",YoN())
            ]
        ).prompt()
        

class Intro(Form):
    async def do_render(self):
        return await prompts.ListPrompt(
            question=I18n_Setting.intro.ques,
            choices=[
                ChoiceBuilder.fromdata("choice01",YoN())
            ]
        ).prompt()