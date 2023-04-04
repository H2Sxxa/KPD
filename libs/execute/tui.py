from abc import ABC,abstractmethod
from asyncio import AbstractEventLoop
from typing import Union
from Remilia.utils.cli import prompts
from Remilia.utils.cli.prompts import DT,RT
from Remilia.lite.LiteLog import Logger


class Form(ABC):
    @abstractmethod
    async def do_render(self) -> Union[DT, RT]:pass
    def form_name(self) -> str:return self.__class__.__name__

class TUI_Builder:
    def __init__(self,loop:AbstractEventLoop,logger:Logger) -> None:
        self.logger=logger
        self.loop=loop
        logger.tui("tui start successfully")

    async def render(self,form:Form):
        self.logger.tui("render",form.form_name())
        result=await form.do_render()
        await self.render(result.data)