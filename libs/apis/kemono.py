from typing import Union,List
from aiohttp import ClientSession
from Remilia.lite.LiteResource import File
from Remilia.lite.utils import typedet
from json import loads,dumps
from lxml.html import fromstring
from base64 import b64encode

from ..yml.app import App_Setting, getCache
from ..utils.instance import getLogger

class DownloadType:
    def __init__(self,name="",url="") -> None:
        self.name=name
        self.url=url
    @staticmethod
    def from_dict(kwargs):
        return DownloadType(**kwargs)

class ImageType:
    def __init__(self,thumb="",raw="") -> None:
        self.thumb=thumb
        self.raw=raw
    @staticmethod
    def from_dict(kwargs):
        return ImageType(**kwargs)

class CommentType:
    def __init__(self,user="",content="",time="",replyto:Union[str,bool]=False) -> None:
        self.user=user
        self.content=content
        self.time=time
        self.replyto=replyto
        
    @staticmethod
    def from_dict(kwargs):
        return CommentType(**kwargs)

class PageContent:
    contents:str=""
    downloads:List[DownloadType]
    files:List[ImageType]
    comments:List[CommentType]
    def __init__(self,downloads,contents,files,comments) -> None:
        self.downloads=downloads
        self.contents=contents
        self.files=files
        self.comments=comments
    @staticmethod
    def from_dict(kwargs):
        return PageContent(**kwargs)

class KemonoClient:
    root = App_Setting.root_site
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
            getLogger().info("pick up cache")
            return loads(contents.text)
        results=await self._handle_html(url)
        contents.write("w",dumps(results))
        return results
    
    async def get_pagecontent(self,url):
        getLogger().debug("handle",url)
        return PageContent.from_dict(await self._handle_content(await self._fetch_html(url)))
    
    async def _fetch_html(self,url):
        async with ClientSession() as clt:
            async with clt.get(url) as rep:
                return await rep.text()
    
    async def _handle_html(self,url):
        logger=getLogger()
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
    
    async def _handle_content(self,text) -> dict:
        seletor=fromstring(text)
        #downloads
        downloads_list=[]
        for li_warp in seletor.xpath("//*[@id=\"page\"]/div/ul[@class=\"post__attachments\"]"):
            for download in li_warp.xpath("li/a"):
                url=download.xpath("@href")[0]
                name=download.xpath("@download")[0]
                getLogger().debug("Get",name,url)
                downloads_list.append(DownloadType(name,url))
        #content
        content=""
        for con_warp in seletor.xpath("//*[@id=\"page\"]/div/div[@class=\"post__content\"]"):
            content=con_warp.xpath("string(.)").strip()
        #Files[image main]
        file_list=[]
        for file_warp in seletor.xpath("//*[@id=\"page\"]/div/div[@class=\"post__files\"]"):
            thumb=self.root+file_warp.xpath("div/a/img[1]/@src")[0]
            raw=file_warp.xpath("div/a/@href")[0]
            getLogger().debug("Get",raw,thumb)
            file_list.append(ImageType(thumb,raw))
        #comments
        #//*[@id="page"]/footer/div
        comments_list=[]
        for comment_warp in seletor.xpath("//*[@id=\"page\"]/footer/div"):
            for comment in comment_warp:
                comment_replyto=comment.xpath("normalize-space(section/div/text())") if comment.xpath("normalize-space(section/div/text())") else False
                comment_user=comment.xpath("normalize-space(header/a/text())")
                comment_content=comment.xpath("normalize-space(section/p/text())")
                comment_time=comment.xpath("normalize-space(footer/time/text())")
                getLogger().debug("Get",comment_time,comment_user,comment_replyto,comment_content)
                if comment_content != "":
                    comments_list.append(CommentType(comment_user,comment_content,comment_time,comment_replyto))
        return {
                "downloads":downloads_list,
                "contents":content,
                "files":file_list,
                "comments":comments_list
                }