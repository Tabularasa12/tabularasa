from secrets import token_hex as secret_key
import configparser
from utils.files import *

__all__ = ['Production', 'Development']

class Config(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///default.sqlite3'
    SECRET_KEY = secret_key()
    MAIL_SERVER = 'smtp.free.fr'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'etienne.mousseau.12'
    MAIL_PASSWORD = 'signer10'

class Production(Config):
    PREFERRED_URL_SCHEME = 'https'
    SERVER_NAME = 'tabularasa.pythonanywhere.com'
    APPLICATION_ROOT = '/'
    DB_CREATE_ALL = False

class Development(Config):
    PREFERRED_URL_SCHEME = ''
    SERVER_NAME = '127.0.0.1:5000'
    APPLICATION_ROOT = '/'
    DB_CREATE_ALL = True

class ConfigFile:
    def __init__(self, path):
        if path.endswith('cfg'):
            self.cfg = configparser.ConfigParser()
            self.path = path
            if not isfile(path):
                self.cfg.write(open(self.path,'w'))
            else:
                self.cfg.read(self.path)
            self.sections = dict()
            for section in self.cfg.sections():
                self.sections[section] = ConfigSection(section, self.path, self.cfg)
        else:
            raise TypeError(f'"{path}" is not a ".cfg" file')
    
    def __getitem__(self, name):
        return self.sections[name]
    def __setitem__(self, name, value):
        if isinstance(value, dict):
            if not name in self.sections.keys():
                self.sections[name] = ConfigSection(name, self.path, self.cfg)
            for k, v in value.items():
                self.sections[name][k] = v
    def __delitem__(self, name):
        self.cfg.remove_section(name)
        self.write
        self.__init__(self.path)

    @property
    def write(self):
        self.cfg.write(open(self.path,'w'))
    
    def __repr__(self):
        return str(self.sections)


class ConfigSection:
    write = ConfigFile.write
    def __init__(self, name, path, cfg):
        self.name = name
        self.path = path
        self.cfg = cfg
        if not self.name in self.cfg.sections():
            self.cfg.add_section(name)
            self.write

    def __getitem__(self, name):
        return self.cfg.get(self.name, name)
    def __setitem__(self, name, value):
        self.cfg.set(self.name, name, value)
        self.write
    def __delitem__(self, name):
        self.cfg.remove_option(self.name,name)
        self.write
    
    def keys(self):
        return self.cfg.options(self.name)

    # def items(self):
    #     return dict(self.cfg.items(self.name)).items()

    # def values(self):
    #     ret = [value for key, value in self.items()]
    #     return ret
    
    def __repr__(self):
        return str(dict(self.cfg.items(self.name)))