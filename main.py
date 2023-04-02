import asyncio
from Remilia.lite.LiteLog import Logger,DefaultStyle
from libs.base import event
from libs.execute import tui

@event.TriggerEvent(event.BoostEvent)
async def main(logger:Logger):
    logger.info("Boost Application in ASYNC!")
    while True:
        tui.TUI_Builder(logger)
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main(Logger(__name__,DefaultStyle.default_LogStyle1)))