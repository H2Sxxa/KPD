from Remilia.lite.v2 import ConfigManager


def getPath(filepath=""):
    return "Data/" + filepath
def geti18n(filepath=""):
    return getPath("i18n/" + filepath)
def getCache(filepath=""):
    return getPath("cache/" + filepath)
def getOut(filepath=""):
    return getPath("out/" + filepath)
def getLog(filepath=""):
    return getPath("log/" + filepath)

App_Conf=ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=getPath("app.yml"),regenerate=True))
@App_Conf
class App_Setting:
    use_alt_ques=False
    log_level=5
    clean_cache=False
    sort_creator=False
    root_site="https://kemono.party"
    lang="en_us.yml"
    @ConfigManager.Cate()
    class generator:
        content_include=["downloads","contents","files","comments"]
        thumb_img=False
    @ConfigManager.Cate()
    class proxy:
        open_proxy=False
        http_proxy="http://127.0.0.1:7890"
        
    @ConfigManager.Cate()
    class aria:
        log_path="./Data/log/aria2c.log"
        args=["./Data/binary/aria2c","--enable-rpc"]
        host="http://localhost"
        port="6800"
        secret=""
        timeout=60.0
    
    @ConfigManager.Cate()
    class glow:
        glow_path="./Data/binary/glow"
        
I18n_Conf=ConfigManager.Config(ConfigManager.ConfigSetting(model=ConfigManager.YamlFile,path=geti18n(App_Setting.lang),regenerate=True))
@I18n_Conf
class I18n_Setting:
    @ConfigManager.Cate()
    class download_status:
        add_uri="Add Uri"
        type_uri="Type Uri"
        ques="Download Status"
    @ConfigManager.Cate()
    class markdown_generator:
        content="Content"
        downloads="Downloads"
        files="Files"
        img_alt="Image Here"
        comments="Comments"
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
        download="Download"
        search="Search"
        setting="Setting"
        exit="Exit"
        
    @ConfigManager.Cate()
    class content:
        printit="Print it"
        glow_open="Open with glow"
        