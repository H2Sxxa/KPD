from Remilia.lite.v2 import ConfigManager
from Remilia.lite.LiteLog import Logger

def getPath(filepath):
    return "Data/" + filepath
def geti18n(filepath):
    return getPath("i18n/" + filepath)
def getCache(filepath):
    return getPath("cache/" + filepath)
def getLog(filepath):
    return getPath("log/" + filepath)

MAIN_LOGGER:Logger=None

App_Conf=ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=getPath("app.yml"),regenerate=True))
@App_Conf
class App_Setting:
    clean_cache=False
    max_cotents=10
    sort_creator=True
    lang="en_us.yml"
    @ConfigManager.Cate()
    class aria:
        log_path="./Data/log/aria2c.log"
        binary="./Data/binary/aria2c.exe"
        args=["--enable-rpc"]
        host="http://localhost"
        port="6800"
        secret=""
        timeout=60.0

I18n_Conf=ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=geti18n(App_Setting.lang),regenerate=True))
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
    class search:
        ques="Type Keyword:"
        warn_empty="Keyword is empty,do you want to continue?"
        plain_search="Plain Search"
        regex_search="Regex Search"
        from_clip="(clip)"
    @ConfigManager.Cate()
    class setting:
        @ConfigManager.Cate()
        class app:
            name="APP Setting"
            clean_cache="Clean cache"
            sort_creator="Sort creators"
        language="Language"
    @ConfigManager.Cate()
    class intro:
        search="Search"
        setting="Setting"
        exit="Exit"