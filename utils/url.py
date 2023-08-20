import re
class URL:
    def __init__(self, *args, _varsdict(), pointer:=''):
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

    def __call__(self):
        url = '/'.join(self.args)
        if self.vars:
            url += '?'
            for k, v in self.vars.items():
                url += f'{k}={v}'
        if self.pointer:
            url += f'#{self.pointer}'
        return url

    def __repr__(self):
        return self()
    
    def __str__(self):
        return self()
