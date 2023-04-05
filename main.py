import asyncio
from Remilia.lite.LiteLog import Logger,DefaultStyle,PrinterStyle,Fore
from Remilia.utils.cli.async_app import MakeAsync
from libs.base import event
from libs.execute import impl, tui

MakeAsync()

@event.TriggerEvent(event.BoostEvent)
async def main(loop:asyncio.AbstractEventLoop,logger:Logger):
    logger.recorder.subscribePath("./Data/log/latest.log")
    logger.addPrintType("tui",4,PrinterStyle.buildLogColor(Fore.CYAN))
    logger.info("Boot Application in ASYNC!")
    while True:
        builder=tui.TUI_Builder(loop,logger)
        await builder.render(impl.Intro())
        
if __name__ == "__main__":
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop,Logger(__name__,DefaultStyle.default_LogStyle1)))