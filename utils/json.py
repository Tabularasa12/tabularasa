import json
from .files import *

class Json:
    def __init__(self, _path, sort_key=True, indent=4, defaults=dict()):
        if _path.endswith('.json'):
            self.sort_key = sort_key
            self.indent = indent
            if not isfile(_path):
                write(_path)
            self.path = _path
            try:
                datas = self.datas
            except:
                datas = dict()
            if isinstance(defaults, dict):
                for k, v in defaults.items():
                    if not k in datas.keys():
                        datas[k] = v
            self.update(datas)
        else:
            raise TypeError(f"{_path} n'est pas un fichier .json")

    def __getitem__(self, name):
        return self.datas[name]

    def __setitem__(self, name, value):
        datas = self.datas
        datas[name] = value
        self.update(datas)
    
    def __delitem__(self, name):
        datas = self.datas
        del datas[name]
        self.update(datas)

    def __repr__(self):
        return str(self.datas)

    @property
    def datas(self):
        with open(self.path, 'r') as json_data:
            datas = json.load(json_data)
        return datas

    def update(self, datas):
        if isinstance(datas, dict):
            with open(self.path, 'w') as json_data:
                json.dump(datas, json_data, sort_keys = self.sort_key, indent = self.indent, ensure_ascii=False)

    def keys(self):
        return self.datas.keys()
    def values(self):
        return self.datas.values()
    def items(self):
        return self.datas.items()

