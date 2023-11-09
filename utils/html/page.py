from flask import url_for

from utils.bulma import bulma
from utils.icons import icons
from utils.json import Json
from settings import *
from utils.functions import labelize

from .ressources import *
from settings import DEFAULT_LOGO_FILE_NAME


DEFAULT_PARAMETERS = dict(
    autor = "Tabularasa",
    charset = "UTF-8",
    description = "Regarder le passé pour construire l'avenir",
    lang = "fr",
    viewport = "width=device-width, initial-scale=1",
    color = 'transparent',
    height = 'fullheight',
    navbar = None,
)

AUTORIZED_HEIGHTS = ['small', 'medium', 'large', 'halfheight', 'fullheight']

class Page(Tagger):
    def __init__(self, app):
        self.config = Json(app.page_config_file_path)
        for k, v in DEFAULT_PARAMETERS.items():
            if not k in self.config.keys():
                self.config[k] = v
        children = [
            HEAD(
                TITLE(app.title, _id='title'),
                META(_name="name", _id='name', _content=app.name),
                META(_name="autor", _id='autor', _content=self.config['autor']),
                META(_name="description", _id='description', _content=self.config['description']),
                META(_name="viewport", _id='viewport', _content=self.config['viewport']),
                META(_charset=self.config['charset'], _id='charset'),
                META(_name="pdfkit-page-size", _id='pdfkit-page-size', _content="A4"),
                META(_name="pdfkit-orientation", _id='pdfkit-orientation', _content="Portrait"),
                LINK(_rel="stylesheet", _type='text/css', _href=url_for('css', filename=bulma.css), _id='bulma'),
                LINK(_rel="stylesheet", _type='text/css', _href=url_for('icons', filename=icons.css), _id='icons'),
                LINK(_rel="icon", _type='image/x-icon', _href=url_for('static', filename=DEFAULT_FAVICON_FILE_NAME), _id='favicon'),
                LINK(_rel="apple-touch-icon", _href=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), _id='logo'),
                _id = 'header'
            ),
            DIV(
                DIV(_id='head', _class='hero-head'),
                Level(_id='body', _class='hero-body'),
                DIV(_id='foot', _class='hero-foot'),
                _class = 'hero is-fullheight',
                _id='content'
            )
        ]
        Tagger.__init__(self, 'HTML', *children)
        self.color = self.config['color']
        self.height = self.config['height']

    def __get_color__(self):
        return self.content.color
    def __set_color__(self, name):
        self.back_color = name
        self.content.color = name
        if self.get_children_by_id('navbar'):
            self.navbar.color = name
    def __del_color__(self):
        del self.content.color
        if self.get_children_by_id('navbar'):
            self.navbar.color = None
    color = property(__get_color__, __set_color__, __del_color__)

    def __get_height__(self):
        for height in ['small', 'medium', 'large', 'halfheight', 'fullheight']:
            if f'is-{height}' in self.content._class.list:
                return height
        return None
    def __set_height__(self, value):
        if value in AUTORIZED_HEIGHTS:
            self.content._class.replace(f'is-{self.__get_height__()}', f'is-{value}')
            # self.config['height'] = value
    def __del_height__(self):
        if name in AUTORIZED_HEIGHTS:
            self.content._class -= f'is-{self.__get_height__()}'
            # self.config['height'] = None
    height = property(__get_height__, __set_height__, __del_height__)

class Masterpage(Page):
    def __init__(self, app):
        Page.__init__(self, app)


class Apppage(Page):
    def __init__(self, app):
        Page.__init__(self, app)
        self._class += 'has-navbar-fixed-top'
        self.body._class += 'is-justify-content-center'
        self.navbar = Navbar(_id='navbar', _class='is-fixed-top has-shadow', color=self.color)
        @app.before_request
        def navbar_init():
            if self.config['navbar']:
                self.navbar_position = self.config['navbar']['position']
            self.navbar.link.update(Image(url=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), text=f"Retour à la liste des applications"), url=url_for('index'))
            def items(side):
                items = []
                for item in self.config['navbar'][side]:
                    name = item['name']
                    help = item['help']
                    icon = item['icon']
                    text = item['text']
                    view = item['view']
                    children = []
                    for v in view:
                        if v == 'icon':
                            children.append(Icon(icon))
                        elif v == 'text':
                            children.append(Text(text, case="capitalized"))
                    items.append(Navitem(*children, url=url_for(f"{app.name}.{name}"), _title=help))
                return items
            
            self.navbar.start.update(*items("left"))
            self.navbar.end.update(*items("right"))
            self.navbar.activate
            self.head.update(self.navbar)

    def __get_navbar_position__(self):
        for position in self.navbar.AUTORIZED_POSITIONS:
            if f'has-navbar-fixed-{position}' in self._class.list:
                return position
        return None
    def __set_navbar_position__(self, name):
        if name in self.navbar.AUTORIZED_POSITIONS:
            hold = self.__get_navbar_position__()
            self._class.replace(f'has-navbar-fixed-{hold}', f'has-navbar-fixed-{name}')
            self.navbar.position = name
            # self.config['navbar'] = name
    def __del_navbar_position__(self):
        hold = self.__get_navbar_position__()
        self._class -= f'has-navbar-fixed-{hold}'
        self.navbar.position = None
        # self.config['navbar'] = None
    navbar_position = property(__get_navbar_position__, __set_navbar_position__, __del_navbar_position__)

