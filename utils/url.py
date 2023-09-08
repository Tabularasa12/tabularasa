import re
from .files import join, sep
# from browser_history import get_history
from flask import request
class URL:
    def __init__(self, *args, _vars=dict(), pointer=''):
        self.args = [*args]
        self.vars=_vars
        self.pointer=str(pointer)
        url = self.args[0]
        if len(self.args) == 1 and not _vars and not pointer:
            if isinstance(url, URL):
                self.__dict__ = copy.deepcopy(url.__dict__)
            if isinstance(url, str):
                url = url.split('?')
                self.args = self.str_to_args(url[0])
                if len(url) > 1:
                    url = url[-1].split('#')
                    self.vars = self.str_to_vars(url[0].split('&'))
                    if len(url) > 1:
                        self.pointer = str_to_pointer(url[1])
    
    def str_to_args(self, args_str):
        args = args_str.strip('/').split('/')
        args = [k for k in args if k != '']
        if args_str.startswith('/'):
            if len(args) > 0:
                args[0] = '/{}'.format(args[0])
            else:
                args = ['/']
        return args
    
    def str_to_vars(self, vars_str):
        vars = dict()
        if vars_str[0]:
            for var in vars_str:
                var = var.split('=')
                vars[var[0]] = var[1]
        return vars
    
    def str_to_pointer(self, pointer_str):
        if re.match('^[a-zA-z]{50}$', pointer_str):
            return pointer_str
        return None

    @property
    def path(self):
        ret = ''
        for arg in self.args:
            ret = join(ret, arg)
        return ret
    
    @property
    def rule(self):
        ret = '.'.join(self.args).strip(sep())
        return ret

    def __call__(self):
        url = '/'.join(self.args)
        if self.vars:
            url += '?'
            for k, v in self.vars.items():
                url += f'{k}={v}'
        if self.pointer:
            url += f'#{self.pointer}'
        return url
    
    def __str__(self):
        return self()

# class History:
#     def __init__(self):
#         self._list = []
    
#     @property
#     def update(self):
#         histories = get_history().histories
#         histories_url = list()
#         for history in histories:
#             histories_url.append(history[-1])
#         routes = list()
#         host = request.host_url.rstrip('/')
#         for _url in histories_url:
#             route = _url.split(host)
#             routes.append(route[-1])
#         self._list = routes
    
#     def __getitem__(self, num):
#         # self.update
#         if len(self._list):
#             return self._list[num]
#         return None
    
#     def __call__(self):
#         # self.update
#         return self._list
    
    # def __str__(self):
    #     ret = 'Historique de navigation :'
    #     for num, el in enumerate(self._list):
    #         ret += f'\n{num} -> {el[0]} -> {el[1]}'
    #     return ret