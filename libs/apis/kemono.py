from aiohttp import ClientSession
from Remilia.lite.LiteResource import File
from Remilia.lite.utils import typedet
from Remilia.lite.v2.InstanceManager import Globals_Instance
from json import loads,dumps
from lxml.html import fromstring
from base64 import b64encode

from libs.base.const import LOGGER_NAME
from ..yml.app import getCache

class KemonoClient:
    root = "https://kemono.party"
    endpoint = root + "/api"

    fanbox = root + "/fanbox/user/"
    fantia = root + "/fantia/user/"
    patreon = root + "/patreon/user/"
    gumroad = root + "/gumroad/user/"
    subscribestar = root + "/subscribestar/user/"
    
    creators= endpoint + "/creators/"
    
    creators_dict={}
    async def get_creator_work(self,root,wid):
        return root+"/post/"+wid
    async def get_creator(self,service,cid):
        return getattr(self,service)+cid
    
    async def fetch_content(self,url):
        contents=File(getCache("content/%s.json"%b64encode(url.encode('utf-8')).decode('utf-8')))
        
        if contents.isexist:
            Globals_Instance.get(LOGGER_NAME).info("pick up cache")
            return loads(contents.text)
        results=await self._handle_html(url)
        contents.write("w",dumps(results))
        return results
    
    async def _fetch_html(self,url):
        async with ClientSession() as clt:
            async with clt.get(url) as rep:
                return await rep.text()
    
    async def _handle_html(self,url):
        logger=Globals_Instance.get(LOGGER_NAME)
        seletor=fromstring(await self._fetch_html(url))
        result=[]
        suburl=[]
        try:
            max_pages=typedet(seletor.xpath("//*[@id=\"paginator-top\"]/small")[0].xpath("normalize-space(text())").split("of ")[1])
            if isinstance(max_pages,int):
                rpgs=max_pages//50
                if max_pages-rpgs > 0 :
                    rpgs+=1
                max_pages=rpgs
        except:
            max_pages=1
        logger.info("Total Page %s"%max_pages)
        for i in range(0,max_pages):
            if i==0:
                pass
            else:
                suburl.append("%s?o=%s"%(url,i*50))
                
        logger.info("Handle Page 1")
        result.extend(await self._handle_seletor(seletor))
        for url in suburl:
            index=suburl.index(url)+2
            logger.info("Handle Page %s"%index)
            result.extend(await self._handle_seletor(fromstring(await self._fetch_html(url))))
        return result
    
    async def _handle_seletor(self,seletor):
        result=[]
        for entry in seletor.xpath("//*[@id=\"main\"]/section/div[3]/div[2]"):
            for div in entry:
                did=div.xpath("@data-id")[0]
                name=div.xpath("normalize-space(a/header/text())")
                result.append({name:did})
        return result
        
    async def fetch_creators(self) -> File:
        creators=File(getCache("creators.json"))
        if not creators.isexist:
            async with ClientSession() as clt:
                async with clt.get(self.creators) as rep:
                    creators.write("w",await rep.text())
        return creators
    
    async def loads_creators(self,text) -> dict:
        self.creators_dict=loads(text)
        return self.creators_dict