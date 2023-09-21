from flask import url_for

from utils.bulma import bulma
from utils.icons import icons
from utils.json import Json
from settings import *
from utils.config import ConfigFile

from .ressources import *
from settings import DEFAULT_LOGO_FILE_NAME

DEFAULT_PARAMETERS = dict(
    color = 'transparent',
    height = 'fullheight',
    navbar = None
)

AUTORIZED_HEIGHTS = ['small', 'medium', 'large', 'halfheight', 'fullheight']

class Page(Tagger):
    def __init__(self, app):
        self.config = ConfigFile(app.page_config_file_path)
        header = self.config['header']
        page = self.config['page']
        children = [
            HEAD(
                TITLE(app.title, _id='title'),
                META(_name="name", _id='name', _content=app.name),
                META(_name="autor", _id='autor', _content=header['autor']),
                META(_name="description", _id='description', _content=header['description']),
                META(_name="viewport", _id='viewport', _content=header['viewport']),
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
        self.color = page['color'] if 'color' in page.keys() else DEFAULT_PARAMETERS['color']
        self.height = page['height'] if 'height' in page.keys() else DEFAULT_PARAMETERS['height']

    def __get_color__(self):
        return self.content.color
    def __set_color__(self, name):
        self.content.color = name
        self.config['color'] = name
    def __del_color__(self):
        del self.content.color
        self.config['color'] = None
    color = property(__get_color__, __set_color__, __del_color__)

    def __get_height__(self):
        for height in ['small', 'medium', 'large', 'halfheight', 'fullheight']:
            if f'is-{height}' in self.content._class.list:
                return height
        return None
    def __set_height__(self, value):
        if value in AUTORIZED_HEIGHTS:
            self.content._class.replace(f'is-{self.__get_height__()}', f'is-{value}')
            self.config['height'] = value
    def __del_height__(self):
        if name in AUTORIZED_HEIGHTS:
            self.content._class -= f'is-{self.__get_height__()}'
            self.config['height'] = None
    height = property(__get_height__, __set_height__, __del_height__)

class Masterpage(Page):
    def __init__(self, app):
        Page.__init__(self, app)


class Apppage(Page):
    def __init__(self, app):
        Page.__init__(self, app)
        self._class += 'has-navbar-fixed-top'
        self.body._class += 'is-justify-content-center'
        
        navbar = Navbar(_id='navbar', _class='is-fixed-top', color=self.color)
        @app.before_request
        def navbar_init():
            navbar.link.update(Image(url=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), text="Retour à la page d'accueil"), url=url_for('index'))
        
        # navbar.burger.text_color = 'white'
        
        # start = []
        # for c in app.controllers:
        #     c_name = c.rsplit('.', 1)[1]
        #     if c_name != 'index':
        #         start.append(Navitem(labelize(c_name), _href=url_for(f'{app.name}.{c_name}')))
        # navbar.start.update(*start)

        # admin = default.blueprints['admin']
        # end = Navitem(Icon('cog', color='white'), _href=url_for(f'{admin.name}.index'))
        # navbar.end.update(end)
        # navbar.activate
        self.head.update(navbar)