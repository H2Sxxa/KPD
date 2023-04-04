import asyncio
from Remilia.lite.LiteLog import Logger,DefaultStyle
from Remilia.utils.cli.async_app import MakeAsync
from libs.base import event
from libs.execute import impl, tui

MakeAsync()

@event.TriggerEvent(event.BoostEvent)
async def main(loop:asyncio.AbstractEventLoop,logger:Logger):
    logger.info("Boost Application in ASYNC!")
    while True:
        builder=tui.TUI_Builder(loop,logger)
        await builder.render(impl.Intro
                             ())
        
if __name__ == "__main__":
    loop=asyncio.get_event_loop()
    loop.run_until_complete(main(loop,Logger(__name__,DefaultStyle.default_LogStyle1)))