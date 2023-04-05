import re,pyperclip
from typing import Union
from os import listdir
from Remilia.utils.cli import prompts

from libs.apis.kemono import KemonoClient
from .tui import Form,TUI_Builder,DT,RT
from ..yml.app import I18n_Setting,getPath,App_Setting,App_Conf
from ..utils.builder import ChoiceBuilder


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
        

class YoN(Form):
    def __init__(self,ques:str=I18n_Setting.global_set.ques) -> None:
        super().__init__()
        self.ques=ques
    async def do_render(self,_:TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=self.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.global_set.as_yes,True),
                ChoiceBuilder.fromdata(I18n_Setting.global_set.as_no,False)
            ]
        ).prompt()
        return ce.data
NRTU=YoN("NOT READY TO USE")
class Intro(Form):
    async def do_render(self,builder:TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.intro.search,Search(self)),
                ChoiceBuilder.fromdata(I18n_Setting.intro.setting,Setting(self)),
                ChoiceBuilder.fromdata(I18n_Setting.intro.exit,Exit(self)),
            ]
        ).prompt()
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
        ).prompt()
        return await builder.render(ce.data)
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
            choices=ChoiceBuilder.fromlist(await kc.fetch_content(url),lambda x:list(x.keys())[0],lambda x:list(x.values())[0])
        ).prompt()
        builder.logger.info(await kc.get_creator_work(url,ce.data))
        return await super().do_render(builder)
    
class Result(CanBackForm):
    def __init__(self, backto: Form,result:list) -> None:
        super().__init__(backto)
        self.result=result
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        lc=ChoiceBuilder.fromlist(self.result,name_warp=lambda x:"%s %s" % (x["name"],x["service"]),data_warp=lambda x:Creator(self,x))
        lc.append(ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto))
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=lc
        ).prompt()
        return await builder.render(ce.data)

class PlainSearch(SearchForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        result=[]
        
        if self.clip:
            keyword=pyperclip.paste()
        else:
            keyword=await prompts.InputPrompt(
                question=I18n_Setting.search.ques
                ).prompt()
            
        
        for creator in self.refer:
            if keyword in creator["name"]:
                builder.logger.info("Get %s" % creator["name"])
                result.append(creator)
        if len(result) == 0:
            builder.logger.info("No Such Creator!")
            return await builder.render(self.backto)
        return await builder.render(Result(self,result))
    
class RegexSearch(SearchForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        result=[]
        if self.clip:
            keyword=pyperclip.paste()
        else:
            keyword=await prompts.InputPrompt(
                question=I18n_Setting.search.ques
                ).prompt()
            
        for creator in self.refer:
            if re.search(keyword,creator["name"]):
                builder.logger.info("Get %s" % creator["name"])
                result.append(creator)
        if len(result) == 0:
            builder.logger.info("No Such Creator!")
            return await builder.render(self.backto)
        return await builder.render(Result(self,result))

class Setting(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=[
                ChoiceBuilder.fromdata(I18n_Setting.setting.language,Lanugage(self)),
                ChoiceBuilder.fromdata(I18n_Setting.global_set.backto,self.backto)
            ]
        ).prompt()
        return await builder.render(ce.data)

class Lanugage(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        ce=await prompts.ListPrompt(
            question=I18n_Setting.global_set.ques,
            choices=ChoiceBuilder.fromlist(listdir(getPath("i18n")))
        ).prompt()
        App_Setting.language._modify("lang",ce.data)
        App_Conf._push(App_Setting)
        return await builder.render(self.backto)

class Exit(CanBackForm):
    async def do_render(self, builder: TUI_Builder) -> Union[DT, RT]:
        if await builder.render(YoN(I18n_Setting.global_set.exit)):
            exit()
        else:
            return await builder.render(self.backto)