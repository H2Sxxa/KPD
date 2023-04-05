from Remilia.lite.v2 import ConfigManager
def getPath(filepath):
    return "Data/" + filepath

App_Conf=ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=getPath("app.yml"),regenerate=True))
@App_Conf
class App_Setting:
    @ConfigManager.Cate()
    class language:
        lang="en_us.yml"
        
def geti18n(filepath):
    return getPath("i18n/" + filepath)

I18n_Conf=ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=geti18n(App_Setting.language.lang),regenerate=True))
@I18n_Conf
class I18n_Setting:
    @ConfigManager.Cate()
    class global_set:
        ques="Choose a choice and return?"
        exit="Confirm to exit"
        backto="Return"
        as_yes="Yes"
        as_no="No"
    @ConfigManager.Cate()
    class setting:
        language="Language"
    @ConfigManager.Cate()
    class intro:
        search="Search"
        setting="Setting"
        exit="Exit"