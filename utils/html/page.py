from flask import url_for

from utils.bulma import bulma
from utils.icons import icons
from utils.parameters import Parameters

from .ressources import *

DEFAULT_PARAMETERS = dict(
    title = 'TITLE',
    name = '',
    autor = '',
    description = '',
    viewport = 'width=device-width, initial-scale=1',
    lang = 'fr',
    charset = "UTF-8",
    color = '',
    logo = 'logo.png',
    favicon = 'favicon.ico',
    height = 'fullheight',
)

AUTORIZED_HEIGHTS = ['small', 'medium', 'large', 'halfheight', 'fullheight']

class Page(Tagger):
    def __init__(self, parameters:dict|Parameters|None=None):
        self.p = Parameters(**parameters, defaults=DEFAULT_PARAMETERS)
        children = [
            HEAD(
                TITLE(self.p.title, _id='title'),
                META(_name="name", _id='name', _content=self.p.name),
                META(_name="autor", _id='autor', _content=self.p.autor),
                META(_name="description", _id='description', _content=self.p.description),
                META(_name="viewport", _id='viewport', _content=self.p.viewport),
                META(_charset=self.p.charset, _id='charset'),
                LINK(_rel="stylesheet", _type='text/css', _href='', _id='bulma'),
                LINK(_rel="stylesheet", _type='text/css', _href='', _id='icons'),
                LINK(_rel="icon", _type='image/x-icon', _href=self.p.favicon, _id='favicon'),
                LINK(_rel="apple-touch-icon", _href=self.p.logo, _id='logo'),
                _id = 'header'
            ),
            DIV(
                DIV(Navbar(_id='navbar'), _class='hero-head', _id='head'),
                DIV(_class='hero-body', _id='body'),
                DIV(DIV('nav', _id='nav', _class='tabs'), _class='hero-foot', _id='foot'),
                _class = 'hero',
                _id='content'
            )
        ]
        Tagger.__init__(self, 'HTML', *children)
        self._class -= __class__.__name__.lower()
        self.height = self.p.height
        if self.height:
            self.content._class += f'is-{self.height}'
    
    def get_color(self):
        return self.content.color
    def set_color(self, name):
        self.content.color = name
    def del_color(self):
        del self.content.color
    color = property(get_color, set_color, del_color)

    def __get_height__(self):
        for height in ['small', 'medium', 'large', 'halfheight', 'fullheight']:
            if f'is-{height}' in self._class.list:
                return height
        return None
    def __set_height__(self, value):
        if value in AUTORIZED_HEIGHTS:
            self._class.replace(f'is-{self.__get_height__()}', f'is-{value}')
    def __del_height__(self):
        if name in AUTORIZED_HEIGHTS:
            self._class -= f'is-{self.__get_height__()}'
    height = property(__get_height__, __set_height__, __del_height__)

    def __call__(self):
        return self.xml()

