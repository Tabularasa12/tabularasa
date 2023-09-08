from flask import url_for

from utils.bulma import bulma
from utils.icons import icons
from utils.json import Json
from settings import *

from .ressources import *

DEFAULT_PARAMETERS = dict(
    name = 'NAME',
    autor = 'AUTOR',
    description = 'DESCRIPTION',
    viewport = 'width=device-width, initial-scale=1',
    lang = 'fr',
    charset = "UTF-8",
    color = 'transparent',
    logo = 'logo.png',
    favicon = 'favicon.ico',
    height = 'fullheight',
    navbar = 'top'
)

AUTORIZED_HEIGHTS = ['small', 'medium', 'large', 'halfheight', 'fullheight']

class Page(Tagger):
    def __init__(self, app):
        config = app.config
        header = config['HEADER']
        children = [
            HEAD(
                TITLE(app.title, _id='title'),
                META(_name="name", _id='name', _content=app.name),
                META(_name="autor", _id='autor', _content=header['autor']),
                META(_name="description", _id='description', _content=header['description']),
                # META(_name="viewport", _id='viewport', _content=header['viewport']),
                META(_charset=header['charset'], _id='charset'),
                META(_name="pdfkit-page-size", _id='pdfkit-page-size', _content="A4"),
                META(_name="pdfkit-orientation", _id='pdfkit-orientation', _content="Portrait"),
                LINK(_rel="stylesheet", _type='text/css', _href=url_for('css', filename=bulma.css), _id='bulma'),
                LINK(_rel="stylesheet", _type='text/css', _href=url_for('icons', filename=icons.css), _id='icons'),
                LINK(_rel="icon", _type='image/x-icon', _href=url_for('static', filename=DEFAULT_FAVICON_FILE_NAME), _id='favicon'),
                LINK(_rel="apple-touch-icon", _href=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), _id='logo'),
                _id = 'header'
            ),
            DIV(
                DIV(_id='head'),
                DIV(_id='body'),
                DIV(_id='foot'),
                _class = 'hero',
                _id='content'
            )
        ]
        Tagger.__init__(self, 'HTML', *children)
        self._class -= __class__.__name__.lower()
        self.color = 'dark'
        self.height = 'fullheight'

    def get_color(self):
        return self.content.color
    def set_color(self, name):
        self.content.color = name
    def del_color(self):
        del self.content.color
    color = property(get_color, set_color, del_color)

    def __get_height__(self):
        for height in ['small', 'medium', 'large', 'halfheight', 'fullheight']:
            if f'is-{height}' in self.content._class.list:
                return height
        return None
    def __set_height__(self, value):
        if value in AUTORIZED_HEIGHTS:
            self.content._class.replace(f'is-{self.__get_height__()}', f'is-{value}')
    def __del_height__(self):
        if name in AUTORIZED_HEIGHTS:
            self.content._class -= f'is-{self.__get_height__()}'
    height = property(__get_height__, __set_height__, __del_height__)

    def xml(self):
        return Tagger.xml(self)

