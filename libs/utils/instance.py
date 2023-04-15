from Remilia.lite.LiteLog import Logger
from Remilia.lite.v2.InstanceManager import from_global
from ..base.const import LOGGER_NAME,ARIA2P_NAME

from aria2p import API

def getLogger() -> Logger:
    return from_global(LOGGER_NAME)

def getAriaAPI() -> API:
    return from_global(ARIA2P_NAME)