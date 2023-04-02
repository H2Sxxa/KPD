from Remilia.lite.v2 import ConfigManager
def getPath(filepath):
    return "Data/" + filepath

@ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=ConfigManager.File(getPath("app.yml")),regenerate=True))
class App_Setting:
    @ConfigManager.Cate()
    class language:
        lang="zh.yml"
        
def geti18n(filepath):
    return getPath("i18n/" + filepath)
@ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=ConfigManager.File(geti18n(App_Setting.language.lang)),regenerate=True))
class I18n_Setting:
    @ConfigManager.Cate()
    class intro:
        ques="Chose it"
        search="search"
        setting="setting"
        exit="exit"