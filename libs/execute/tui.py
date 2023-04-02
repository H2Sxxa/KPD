from abc import ABC,abstractmethod
from Remilia.utils.cli import prompts
from Remilia.lite.LiteLog import Logger
class Form(ABC):
    @abstractmethod
    async def do_render(self) -> None:pass
    @abstractmethod
    async def form_name(self) -> str:pass

class TUI_Builder:
    def __init__(self,logger:Logger) -> None:
        self.logger=logger
        logger.tui("tui start successfully")
    
    async def render(self,form:Form):
        self.logger.tui("render",form.form_name)
        await form.do_render()