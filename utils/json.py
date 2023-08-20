import json
from os.path import isfile

class Json:
    def __init__(self, _path, **objects):
        if not isfile(_path):
            with open(_path, 'w') as json_data:
                json.dump(dict(), json_data, sort_keys = True, indent = 4)
        self.path = _path

        if objects:
            for k, v in objects.items():
                if not k in self.keys():
                    self[k] = v

    def json_to_obj(self):
        with open(self.path, 'r') as json_data:
            datas = json.load(json_data)
        return datas

    def obj_to_json(self, name, value):
        content = self.json_to_obj()
        content[name] = value
        with open(self.path, 'w') as json_data:
            json.dump(content, json_data, sort_keys = True, indent = 4)

    def __getitem__(self, name):
        return self.content[name]

    def __setitem__(self, name, value):
        self.obj_to_json(name, value)
    
    def __delitem__(self, name):
        content = self.content
        del content[name]
        with open(self.path, 'w') as json_data:
            json.dump(content, json_data, sort_keys = True, indent = 4)
    
    def get_content(self):
        return self.json_to_obj()
    def set_content(self, dict):
        self.del_content()
        for k, v in dict.items():
            self.__setitem__(k, v)
    def del_content(self):
        for i in self.get_content().keys():
            self.__delitem__(i)
    content = property(get_content, set_content, del_content)

    def keys(self):
        return self.content.keys()
    def values(self):
        return self.content.values()
    def items(self):
        return self.content.items()

    def __repr__(self):
        return str(self.content)
