import aria2p
import subprocess,threading

from Remilia.lite.v2.InstanceManager import Globals_Instance
from Remilia.lite.LiteLog import Logger
from ...yml.app import App_Setting
from ...base.const import ARIA2P_NAME

class AriaAdapter:
    def __init__(self,logger:Logger) -> None:
        self.logger=logger
        self.host=App_Setting.aria.host
        self.port=App_Setting.aria.port
        self.secret=App_Setting.aria.secret
        self.timeout=App_Setting.aria.timeout
        
    @staticmethod
    def __lock_thread():
        boost_args=App_Setting.aria.args
        boost_args.insert(0,App_Setting.aria.binary)
        with open(App_Setting.aria.log_path,"w") as logout:
            subprocess.Popen(boost_args,stderr=logout,stdout=logout).wait()
            
    async def init_adapter(self):
        await self.launch_client()
        await self.refresh_api()
        return self
    
    async def launch_client(self):
        self.logger.info("init AriaAdapter")
        threading.Thread(target=self.__lock_thread).start()
        return self
    
    async def refresh_api(self):
        self.logger.info("refresh aria API")
        api=aria2p.API(
            aria2p.Client(self.host,self.port,self.secret,self.timeout)
        )
        
        Globals_Instance.add(ARIA2P_NAME,api)
        
        return api