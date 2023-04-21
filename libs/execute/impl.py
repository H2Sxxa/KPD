import re,pyperclip
from typing import List, Union
from os import listdir
from Remilia.utils.cli import prompts
from Remilia.base.files import File

from .tui import Form,TUI_Builder,DT,RT
from ..apis.kemono import KemonoClient
from ..utils.instance import getAriaAPI
from ..utils import handle_exit
from ..utils.builder import ChoiceBuilder, MarkDownBuilder
from ..yml.app import I18n_Setting,getPath,App_Setting,App_Conf,I18n_Conf,geti18n,getOut

class CanBackForm(Form):
    def __init__(self,backto:Form) -> None:
        super().__init__()
        self.backto=backto
        
class SearchForm(Form):
    def __init__(self,backto:Form,refer:dict,clip=False) -> None:
        super().__init__()
        self.backto=backto
        self.refer=refer
        self.clip=clip
        
    async def get_keyword(self,builder:TUI_Builder) -> str:
        if self.clip:
            keyword=pyperclip.paste()
        else:
            keyword=await prompts.InputPrompt(
                question=I18n_Setting.search.ques
                ).prompt_async()
        if keyword == "":
            if not await builder.render(YoN(I18n_Setting.search.warn_empty)):
                await builder.render(self)
        return keyword
    
class SettingForm(Form):
    def setBack(self,obj):
        self.backto=obj
        return self
class ALTCForm(SettingForm):
    def __init__(self,name:str) -> None:
        super().__init__()
        self.name=name
    def do_overwrite(self,obj):
        App_Conf._modify_push(self.name,obj)
    
class YoN(Form):
    def __init__(self,ques:str=I18n_Setting.global_set.ques) -> None:
        super().__init__()
        self.ques=ques
    async def do_render(self,_:TUI_Builder) -> Union[DT, RT]:
        if App_Setting.use_alt_ques:
            return await prompts.ConfirmPrompt(
            question=self.ques,
        ).prompt_async()

        ce=await prompts.ListPrompt(
            question=self.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.global_set.as_yes,True),
                ChoiceBuilder.fromdata(I18n_Setting.global_set.as_no,False)
            ]
        ).prompt_async()
        return ce.data
NRTU=YoN("NOT READY TO USE")
class Intro(Form):
    async def do_render(self,builder:TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.intro.search,Search(self)),
                ChoiceBuilder.fromdata(I18n_Setting.intro.download,DownloadStatus(self)),
                ChoiceBuilder.fromdata(I18n_Setting.intro.setting,Setting(self)),
                ChoiceBuilder.fromdata(I18n_Setting.intro.exit,Exit(self)),
            ]
        ).prompt_async()
        return await builder.render(ce.data)

class Search(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        kc=KemonoClient()
        builder.logger.info("Fetch Creators...")
        creators_file=await kc.fetch_creators()
        creators_dict=await kc.loads_creators(creators_file.text)
        builder.logger.info("Fetch Finish!")
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.search.plain_search,PlainSearch(self,creators_dict)),
                ChoiceBuilder.fromdata(I18n_Setting.search.regex_search,RegexSearch(self,creators_dict)),
                ChoiceBuilder.fromdata(I18n_Setting.search.plain_search+I18n_Setting.search.from_clip,PlainSearch(self,creators_dict,True)),
                ChoiceBuilder.fromdata(I18n_Setting.search.regex_search+I18n_Setting.search.from_clip,RegexSearch(self,creators_dict,True)),
                ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto)
            ]
        ).prompt_async()
        return await builder.render(ce.data)
class DownloadStatus(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        lines=ChoiceBuilder.fromlist(getAriaAPI().get_downloads(),lambda download:download.name +" | "+download.progress_string()+" ["+download.download_speed_string()+"]",lambda _:DownloadStatus(self.backto))
        lines.append(ChoiceBuilder.fromdata(I18n_Setting.download_status.add_uri,TypeUri(self.backto)))
        lines.append(ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto))
        le=await prompts.ListPrompt(
            question=I18n_Setting.download_status.ques,
            choices=lines
        ).prompt_async()
        return await builder.render(le.data)
    
class TypeUri(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        uri=await prompts.InputPrompt(
            question=I18n_Setting.download_status.type_uri
        ).prompt_async()
        try:
            getAriaAPI().add(uri)
        except Exception as e:
            builder.logger.error(e)
        return await builder.render(DownloadStatus(self.backto))
class Content(CanBackForm):
    def __init__(self, backto: Form,url:str,name="") -> None:
        super().__init__(backto)
        self.url=url
        self.name=name
    async def getChoices(self):
        res=[]
        res.append(ChoiceBuilder.fromdata(I18n_Setting.content.printit,lambda text:print(text)))
        res.append(ChoiceBuilder.fromdata(I18n_Setting.content.glow_open,lambda _:None))
        return res
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        kc=KemonoClient()
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=await self.getChoices()
        ).prompt_async()
        pct=await kc.get_pagecontent(self.url)
        md=await MarkDownBuilder(pct).getText()
        File(getOut(f"{self.name}.md")).write("w",md)
        ce.data(md)
        return await builder.render(self.backto)

class Creator(CanBackForm):
    def __init__(self, backto: Form,result:list) -> None:
        super().__init__(backto)
        self.result=result
    
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        builder.logger.debug("handle",self.result)
        kc=KemonoClient()
        url=await kc.get_creator(self.result["service"],self.result["id"])
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=ChoiceBuilder.fromlist(await kc.fetch_content(url),lambda x:list(x.keys())[0],lambda x:list(x.values())[0]) + [ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto),]
        ).prompt_async()
        if isinstance(ce.data,Form):
            return await builder.render(ce.data)
        return await builder.render(Content(self,await kc.get_creator_work(url,ce.data),ce.name))
    
class Result(CanBackForm):
    def __init__(self, backto: Form,result:list) -> None:
        super().__init__(backto)
        self.result=result
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=ChoiceBuilder.fromlist(self.result,name_warp=lambda x:"%s %s" % (x["name"],x["service"]),data_warp=lambda x:Creator(self,x)) + [ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto),]
        ).prompt_async()
        return await builder.render(ce.data)

class PlainSearch(SearchForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        result=[]
        
        keyword=await self.get_keyword(builder)
        
        for creator in self.refer:
            if keyword in creator["name"]:
                builder.logger.info("Get %s" % creator["name"])
                result.append(creator)
        if App_Setting.sort_creator:result.sort(key=lambda x:x["name"])
        if len(result) == 0:
            builder.logger.info("No Such Creator!")
            return await builder.render(self.backto)
        return await builder.render(Result(self,result))
    
class RegexSearch(SearchForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        result=[]
        
        keyword=await self.get_keyword(builder)
            
        for creator in self.refer:
            if re.search(keyword,creator["name"]):
                builder.logger.info("Get %s" % creator["name"])
                result.append(creator)
        if App_Setting.sort_creator:result.sort(key=lambda x:x["name"])
        if len(result) == 0:
            builder.logger.info("No Such Creator!")
            return await builder.render(self.backto)
        return await builder.render(Result(self,result))

class Setting(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.setting.language,Language(self)),
                ChoiceBuilder.fromdata(I18n_Setting.setting.app.name,SubSettingPage(self).set_choice([
                        ChoiceBuilder.fromdata(I18n_Setting.setting.app.clean_cache,BoolSetting("clean_cache")),
                        ChoiceBuilder.fromdata(I18n_Setting.setting.app.sort_creator,BoolSetting("sort_creator"))
                        ]
                    )
                                       ),
                ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto)
            ]
        ).prompt_async()
        return await builder.render(ce.data)
class SubSettingPage(CanBackForm):
    choices=[]
    def set_choice(self,choices:List[prompts.Choice]):
        self.choices=choices
        self.choices.append(ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto))
        for cs in self.choices:
            if isinstance(cs.data,SettingForm):
                cs.data.setBack(self)
        return self
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=self.choices
        ).prompt_async()
        
        return await builder.render(ce.data)
    
class Language(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=ChoiceBuilder.fromlist(listdir(getPath("i18n")))
        ).prompt_async()
        App_Conf._modify_push("lang",ce.data)
        I18n_Conf._setting.replace_ins(geti18n(ce.data))
        I18n_Conf._get(I18n_Conf._obj)
        return await builder.render(self.backto)

class BoolSetting(ALTCForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        self.do_overwrite(await builder.render(YoN()))
        return await builder.render(self.backto)


class Exit(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        if await builder.render(YoN(I18n_Setting.global_set.exit)):
            handle_exit()
        else:
            return await builder.render(self.backto)