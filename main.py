import asyncio
from shutil import rmtree
from Remilia.lite.LiteLog import Logger,DefaultStyle,PrinterStyle,Fore
from Remilia.utils.cli.async_app import MakeAsync
from Remilia.lite.v2.DictoryTreeBuilder import DictroyTree,Node

from libs.base import event
from libs.execute import impl, tui
from libs.yml.app import App_Setting

MakeAsync()

if App_Setting.clean_cache:
    rmtree("Data/cache")

@DictroyTree
class Data:
    @Node
    class i18n:pass
    @Node
    class log:pass
    @Node
    class cache:
        @Node
        class content:pass
    @Node
    class out:pass

@event.TriggerEvent(event.BoostEvent)
async def main(loop:asyncio.AbstractEventLoop,logger:Logger):
    logger.recorder.subscribePath("./Data/log/latest.log")
    logger.addPrintType("tui",4,PrinterStyle.buildLogColor(Fore.CYAN))
    logger.info("Boot Application in ASYNC!")
    while True:
        builder=tui.TUI_Builder(loop,logger)
        await builder.render(impl.Intro())
        
if __name__ == "__main__":
    logger=Logger(__name__,DefaultStyle.default_LogStyle1)
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop,logger))