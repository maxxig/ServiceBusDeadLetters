import configparser
#get config
def get_config():
    config = configparser.ConfigParser()
    config.sections()
    config.read('config.ini', encoding="utf-8")
    return config['parameters']