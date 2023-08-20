from .files import *
import importlib
import json
import copy
from easydict import EasyDict as edict

class Parameters(edict):
    def __init__(self, defaults=None, **values):
        ret = self.__obj_to_dict__(copy.copy(defaults)) if defaults else {}
        for k, v in values.items():
            ret[k] = v
        edict.__init__(self, **ret)
    
    def __obj_to_dict__(self, _object=''):
        ret = None
        if isinstance(_object, str):
            if isfile(_object):
                if ext(_object) == '.py':
                    ret = self.__from_pyfile__(_object)
                elif ext(_object) == '.json':
                    ret = self.__from_jsonfile__(_object)
            else:
                raise FileNotFoundError(f'{_object} does not exist !!!')
        elif isinstance(_object, dict):
            ret = _object
        elif isinstance(_object, (list, tuple)):
            if len(_object) == 2:
                if isinstance(_object[0], str):
                    if isinstance(_object[1], (int, float, str, list, tuple, dict)):
                        ret = {f'{_object[0]}': _object[1]}                
        if not ret:
            raise NotImplementedError(f'{_object} is not a correct object for {__class__.__name__} Class: (str | list(name, value) | tuple(name, value) | dict)')
        return ret

    @staticmethod
    def __from_pyfile__(path):
        path = path.strip('.py').replace(sep(), '.')
        file = importlib.import_module(path)
        ret = dict()
        for k, v in file.__dict__.items():
            if not k.startswith('__'):
                ret[k] = v
        return ret

    @staticmethod
    def __from_jsonfile__(path):
        with open(path, 'r') as json_data:
            ret = json.load(json_data)
        return ret
