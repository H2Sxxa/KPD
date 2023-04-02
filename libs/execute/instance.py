from .tui import Form,prompts
from ..yml import i18n
class intro(Form):
    async def do_render(self) -> None:
        prompts.ListPrompt(
            question=i18n.i18n.intro.ques
        )
        return await super().do_render()