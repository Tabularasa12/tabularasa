from flask import request
from utils.url import URL
from .taggers import Tagger, DIV, SPAN
from .elements import Button

__all__ = ['Navitem', 'Navbar', 'Divider', 'Dropdown']
__all__ = ['Navitem', 'Navbar']

class Burger(Button):
    def __init__(self, name, **attributes):
        children = [SPAN(), SPAN(), SPAN()]
        attributes = dict(_role='button', _class="navbar-burger", **attributes)
        attributes["data-target"] = name
        attributes["aria-label"] = "menu"
        attributes["aria-expanded"] = "false"
        Button.__init__(self, *children, **attributes)

class Navitem(Button):
    def __init__(self, *children, **attributes):
        Button.__init__(self, *children, **attributes)
        self._class.replace('navitem', 'navbar-item icon-text')
    #     self.title = attributes['title'] if 'title' in attributes.keys() else None
    #     self.url = attributes['url'] if 'url' in attributes.keys() else '/'

    # def get_title(self):
    #     return self.attributes['_title']
    # def set_title(self, name):
    #     self.attributes['_title'] = name
    # def del_title(self):
    #     self.attributes['_title'] = None
    # title = property(get_title, set_title, del_title)

    def activate(self):
        self._class += 'is-active'

    def desactivate(self):
        self._class -= 'is-active'

# class Divider(Tagger):
#     def __init__(self, *children, **attributes):
#         Tagger.__init__(self, *children, **attributes, _base='HR')
#         self._class.replace('divider', "navbar-divider")

# class Dropdown(Navitem):
#     def __init__(self, title=None, *children, **attributes):
#         self.link = A(title, _class="navbar-link")
#         self.list = DIV(*children, _class="navbar-dropdown")
#         Navitem.__init__(self, self.link, self.list, **attributes)
#         self._class.replace('dropdown', 'is-hoverable')
    
    # @property
    # def activate(self): 
    #     if activate(self.list.children):
    #         self.link._class += 'is-active'

class Navbar(Tagger):
    def __init__(self, starts=[], ends=[], **attributes):
        if not isinstance(starts, list): starts=[starts]
        if not isinstance(ends, list): ends=[ends]

        children=[
            DIV(
                Navitem(_id='link'),
                Burger('menu', _id='burger'),
                _class="navbar-brand",
                _id='brand'
            ),
            DIV(
                DIV(*starts, _class="navbar-start", _id='start'),
                DIV(*ends, _class="navbar-end", _id='end'),
                _class="navbar-menu",
                _id='menu'
            ),
        ]
        attributes["_role"] = "navigation"
        attributes["_aria-label"] = "main navigation"
        Tagger.__init__(self, 'nav', *children, **attributes)
        self._class += "is-fullhd"

    @property
    def open(self):
        self.burger['_href'] = request.url_rule
        self.menu._class += "is-active"
        self.burger._class += "is-active"

    @property
    def close(self):
        url = URL(request.full_path)
        url.vars['navbar'] = 'open'
        self.burger['_href'] = url()
        self.menu._class -= "is-active"
        self.burger._class -= "is-active"

    @property
    def activate(self):
        if request.args.get('navbar') == 'open':
            self.open
        else:
            self.close