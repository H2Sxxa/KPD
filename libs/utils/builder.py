from typing import List
from Remilia.utils.cli import prompts

from ..yml.app import App_Setting,I18n_Setting


class ChoiceBuilder:
    @staticmethod
    def fromdata(name:str,data) -> prompts.Choice:
        return prompts.Choice(name,data)
    
    @staticmethod
    def fromlist(target:list,name_warp=lambda _:_,data_warp=lambda _:_) -> List[prompts.Choice]:
        return [prompts.Choice(name_warp(name),data_warp(name)) for name in target]

class MarkDownBuilder:
    def __init__(self,pct) -> None:
        self.sequence=App_Setting.generator.content_include
        self.pct=pct
        self.subtitlelevel=2
    async def getText(self):
        '''
        content_include:
        - downloads
        - contents
        - files
        - comments
        '''
        res=[]
        for part_name in self.sequence:
            if hasattr(self.pct,part_name):
                if part_name == "contents":
                    res.append(await self.getContent())
                elif part_name == "files":
                    res.append(await self.getFiles())
                elif part_name == "downloads":
                    res.append(await self.getDownloads())
                elif part_name == "comments":
                    res.append(await self.getComments())
                else:pass
        return "\n".join(res)
    
    def subtitle(self,x):
        return "#"*x+" "
    
    def combine(self,title,x):
        return title+"\n\n"+x+"\n"
    
    def warp_txt_withurl(self,txt,url):
        return "[%s](%s)" % (txt,url)
    
    def warp_img(self,url):
        return "![%s](%s)" % (I18n_Setting.markdown_generator.img_alt,url)
    
    async def getContent(self):
        return self.combine(self.subtitle(self.subtitlelevel)+I18n_Setting.markdown_generator.content,self.pct.contents)
    
    async def getDownloads(self):
        return self.combine(self.subtitle(self.subtitlelevel)+I18n_Setting.markdown_generator.downloads,"\n\n".join([self.warp_txt_withurl(download.name,download.url) for download in self.pct.downloads]))
    
    async def getFiles(self):
        return self.combine(self.subtitle(self.subtitlelevel)+I18n_Setting.markdown_generator.files,"\n\n".join([self.warp_img(x.thumb) for x in self.pct.files]) if App_Setting.generator.thumb_img else "\n\n".join([self.warp_img(x.raw) for x in self.pct.files]))
    
    async def getComments(self):
        res=[]
        for x in self.pct.comments:
            if x.replyto:
                res.append("%s | %s -> %s :%s"%(x.time,x.user,x.replyto,x.content))
            else:
                res.append("%s | %s :%s"%(x.time,x.user,x.content))  
        return self.combine(self.subtitle(self.subtitlelevel)+I18n_Setting.markdown_generator.comments,"\n\n".join(res))