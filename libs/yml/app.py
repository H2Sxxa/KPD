from Remilia.lite.v2 import ConfigManager
def getPath(filepath):
    return "Data/" + filepath

@ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=getPath("app.yml"),regenerate=True))
class App_Setting:
    @ConfigManager.Cate()
    class language:
        lang="en_us.yml"
        
def geti18n(filepath):
    return getPath("i18n/" + filepath)
@ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=geti18n(App_Setting.language.lang),regenerate=True))
class I18n_Setting:
    @ConfigManager.Cate()
    class global_set:
        ques=""
    @ConfigManager.Cate()
    class intro:
        ques="Chose it"
        search="search"
        setting="setting"
        exit="exit"