from .helpers import TAGGER
from copy import copy
from settings import DEFAULT_SIZE
from utils.functions import strip_list

TAGS = [
    "A",
    "DIV",
    "BODY",
    "FORM",
    "HEAD",
    "HTML",
    "HR",
    "IMG",
    "INPUT",
    "BUTTON",
    "LABEL",
    "LI",
    "OL",
    "OPTION",
    "P",
    "SELECT",
    "SECTION",
    "SPAN",
    "TABLE",
    "THEAD",
    "TBODY",
    "TD",
    "TEXTAREA",
    "TH",
    "TT",
    "TR",
    "UL",
    "I",
    "META",
    "LINK",
    "TITLE",
]

__all__ = TAGS +['Tagger', 'AUTORIZED_COLORS', 'str_2_tagger']

def str_2_tagger(tagger):
    def is_tagger_str(tagger):
        if isinstance(tagger, str):
            tagger = tagger.strip()
            if tagger.startswith('<') and tagger.endswith('>'): return tagger
            else: return False
        else: raise TypeError(f'{tagger} is not a string')

    def get_name(tagger):
        tagger = is_tagger_str(tagger)
        if tagger:
            tagger_split = strip_list(tagger.split('>', 1))
            start = tagger_split[0].lstrip('<')
            elements = strip_list(start.split(' '))
            return elements[0]
        return None

    def get_attributes(tagger):
        tagger = is_tagger_str(tagger)
        if tagger:
            attributes = dict()
            elements = tagger.strip(f'<{get_name(tagger)}').split('>', 1)[0].strip().split(' ')
            for element in elements:
                element = element.split('=')
                if len(element) == 2:
                    attributes[f'_{element[0]}'] = element[1].strip("\'").strip('\"')
                elif element[0]:
                    attributes[f'_{element[0]}'] = element[0]
            return attributes
        return None

    def get_children(tagger):
        tagger_str = is_tagger_str(tagger)
        if tagger_str:
            tagger = tagger_str
            children = []
            elements = strip_list(tagger.split('>', 1))
            if len(elements) == 2:
                elements = elements[1].split(f'</{get_name(tagger)}>', 1)
                if elements[0]:
                    childs = elements[0].strip()
                    child = first_child(childs)
                    while child:
                        children.append(child)
                        childs = childs.split(child, 1)[1]
                        child = first_child(childs)
            return children
        return [tagger]

    def first_child(string):
        string = string.strip()
        if '<' in string and '>' in string:
            elements = string.split('<', 1)
            if elements[0]:
                return elements[0]
            else:
                name = get_name(f'<{elements[1]}')
                tagger = string.split(f'</{name}>', 1)
                if len(tagger) == 2:
                    return f'{tagger[0]}</{name}>'
                else:
                    tagger = tagger[0].split('>', 1)[0]
                    return f'{tagger}>'
        else:
            return string

    tagger_str = is_tagger_str(tagger)
    if tagger_str:
        children = get_children(tagger_str)
        for num, child in enumerate(children):
            children[num] = str_2_tagger(child)
        return Tagger(get_name(tagger_str), *children, **get_attributes(tagger_str))
    else:
        return tagger

class Text_attr:
    types_sep = dict(
        _class = " ",
        _style = ";"
    )
    def __init__(self, *string, _class):
        self.sep = self.types_sep["_{}".format(_class.__name__.lower())]
        self._class = _class
        self.string = string

    def __get_string__(self):
        return self.__dict__['string']
    def __set_string__(self, object):
        self.__dict__['string'] = self.secure(*object)
    string = property(__get_string__, __set_string__)

    def secure(self, *objects):
        strings = []
        for object in objects:
            if not object:
                object = ''
            if isinstance(object, str):
                strings += object.strip().split(self.sep)
            elif isinstance(object, self._class):
                strings += object.string.split(self.sep)
            else:
                raise TypeError("{} must be a {} not {}".format(object, self._class, type(object)))
        ret = "{}".format(self.sep.join(strings))
        if ret:
            ret = '{}{}'.format(ret, self.sep if ret[-1] != self.sep else '')
            if ret[-1] == ' ': ret = ret[:-1]
        return ret
    
    @property
    def list(self):
        return self.get_list(self.string)

    def get_list(self, string):
        return [s for s in string.split(self.sep) if s]

    def append(self, object):
        hold_strings = self.get_list(self.string)
        new_strings = self.get_list(self.secure(object))
        self.string = hold_strings + [s for s in new_strings if s not in hold_strings]
    
    def delete(self, object):
        hold_strings = self.get_list(self.string)
        new_strings = self.get_list(self.secure(object))
        self.string = [s for s in hold_strings if s not in new_strings]

    def replace(self, hold, new):
        self.delete(hold)
        self.append(new)    

    def __add__(self, object):
        self.append(object)
    def __radd__(self, object):
        self.__add__(object)
        return self
    def __iadd__(self, object):
        self.__add__(object)
        return self

    def __sub__(self, object):
        self.delete(object)
    def __rsub__(self, object):
        self.__sub__(object)
        return self
    def __isub__(self, object):
        self.__sub__(object)
        return self
    
    def __eq__(self, object):
        new_string = object.string if isinstance(object, self._class) else object
        return True if self.secure(self.string) == self.secure(new_string) else False
    def __req__(self, object):
        return self.__eq__(object)

    def __ne__(self, object):
        return not self.__eq__(object)
    def __rne__(self, object):
        return self.__rne__(object)

    def __repr__(self):
        return str(self.string)
    
    def xml(self):
        return str(self.string)

class Class(Text_attr):
    def __init__(self, *obj):
        Text_attr.__init__(self, *obj, _class = self.__class__)

class Style(Text_attr):
    def __init__(self, *obj):
        Text_attr.__init__(self, *obj, _class = self.__class__)


AUTORIZED_COLORS = [
    'primary',
    'link',
    'info',
    'success',
    'warning',
    'danger',
    'white',
    'dark',
    'transparent',
]

NBR_OF_SIZE = 7

class Tagger(TAGGER):
    AUTORIZED_SIZES = range(1, (NBR_OF_SIZE+1))
    def __init__(self,
        name,
        *children,
        _class='',
        _style='',
        color='',
        back_color='',
        text_color='',
        size='',
        **attributes
        ):
        children = [*children] if children else []
        TAGGER.__init__(self, name, *children, **attributes)
        self._class = _class
        self._style = _style
        if color: self.color = color
        if back_color: self.back_color = back_color
        if text_color: self.text_color = text_color
        if size: self.size = size
    
    def __get_color__(self):
        for color in AUTORIZED_COLORS:
            if f'is-{color}' in self._class.list:
                return color
        return None
    def __set_color__(self, name):
        if name in AUTORIZED_COLORS:
            self._class.replace(f'is-{self.__get_color__()}', f'is-{name}')
    def __del_color__(self):
        self._class -= f'is-{self.__get_color__()}'
    color = property(__get_color__, __set_color__, __del_color__)

    def __get_back_color__(self):
        for color in AUTORIZED_COLORS:
            if f'has-background-{color}' in self._class.list:
                return color
        return None
    def __set_back_color__(self, name):
        if name in AUTORIZED_COLORS:
            self._class.replace(f'has-background-{self.__get_back_color__()}', f'has-background-{name}')
    def __del_back_color__(self):
        self._class -= f'has-background-{self.__get_back_color__()}'
    back_color = property(__get_back_color__, __set_back_color__, __del_back_color__)

    def __get_text_color__(self):
        for color in AUTORIZED_COLORS:
            if f'has-text-{color}' in self._class.list:
                return color
        return None
    def __set_text_color__(self, name):
        if name in AUTORIZED_COLORS:
            self._class.replace(f'has-text-{self.__get_text_color__()}', f'has-text-{name}')
    def __del_text_color__(self):
        self._class -= f'has-text-{self.__get_text_color__()}'
    text_color = property(__get_text_color__, __set_text_color__, __del_text_color__)

    def __get_size__(self):
        for size in self.AUTORIZED_SIZES:
            if f'is-size-{size}' in self._class.list:
                return size
        return None
    def __set_size__(self, name):
        if name in self.AUTORIZED_SIZES:
            self._class.replace(f'is-size-{self.__get_size__()}', f'is-size-{name}')
    def __del_size__(self):
        self._class -= f'is-size-{self.__get_size__()}'
    size = property(__get_size__, __set_size__, __del_size__)

    def get_children_by_id(self, key):
        return self.find(f'#{key}')

    def __getattr__(self, name):
        childs = self.get_children_by_id(name)
        if isinstance(childs, list) and len(childs) == 1:
            return childs[0]
        return object.__getattr__(self, name)
    
    def __delattr__(self, name):
        childs = self.get_children_by_id(name)
        if isinstance(childs, list) and len(childs) == 1:
            for i, c in enumerate(self.children):
                if c == childs[0]:
                    del self.children[1]
        else:
            object.__delattr__(self, name)

    def update(self, *children, **attributes):
        self.children = [*children] if children else copy(self.children)
        for key, value in attributes.items():
            if key.startswith('_'):
                self.attributes[key] = value
            else:
                exec(f'self.{key}="{value}"')

    def get_class(self): return self['_class']
    def set_class(self, value): self['_class'] = Class(value)
    def del_class(self): self['_class'] = Class('')
    _class = property(get_class, set_class, del_class)

    def get_style(self): return self['_style']
    def set_style(self, value): self['_style'] = Style(value)
    def del_style(self): self['_style'] = Style('')
    _style = property(get_style, set_style, del_style)

    @property
    def hide(self):
        self._class += 'is-hidden'

class METATAG:
    def __getattr__(self, name):
        return self[name]

    def __getitem__(self, name):
        return lambda *children, **attributes: Tagger(name, *children, **attributes)

TAG = METATAG()
DIV = TAG.div
SPAN = TAG.span
LI = TAG.li
OL = TAG.ol
UL = TAG.ul
I = TAG.i
A = TAG.a
P = TAG.p
H1 = TAG.h1
H2 = TAG.h2
H3 = TAG.h3
H4 = TAG.h4
H5 = TAG.h5
H6 = TAG.h6
EM = TAG.em
TR = TAG.tr
TD = TAG.td
TH = TAG.th
TT = TAG.tt
PRE = TAG.pre
CODE = TAG.code
FORM = TAG.form
HEAD = TAG.head
HTML = TAG.html
HR = TAG.hr
BODY = TAG.body
TABLE = TAG.table
THEAD = TAG.thead
TBODY = TAG.tbody
LABEL = TAG.label
STYLE = TAG.style
STRONG = TAG.strong
SELECT = TAG.select
SECTION = TAG.section
OPTION = TAG.option
TEXTAREA = TAG.textarea
BUTTON = TAG.button
TITLE = TAG.title
PROGRESS = TAG.progress
IMG = TAG["img/"]
INPUT = TAG["input/"]
META = TAG["meta/"]
LINK = TAG["link/"]
