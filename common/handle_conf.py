import os
from configparser import ConfigParser
from common.handle_path  import CONF_DIR

class Config(ConfigParser):
    def __init__(self, conf_file):
        super().__init__()
        self.read(conf_file, encoding='utf-8')


conf = Config(os.path.join(CONF_DIR,'config.ini'))
# if __name__ == '__main__':
#     conf = ConfigParser()
#     conf.read(r'E:\pywork_space\py35_17day\config.ini',encoding='utf-8')
#     conf = Config(r'E:\pywork_space\py35_17day\config.ini')
#     name = conf.get('logging', 'name')
#     level = conf.get('logging', 'level')
#     filename = conf.get('logging', 'filename')
#     sh_level = conf.get('logging', 'sh_level')
#     fh_level = conf.get('logging', 'fh_level')
#     print(name)
#     print(level)
#     print(filename)
#     print(sh_level)
#     print(fh_level)
