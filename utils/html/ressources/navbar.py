from flask import redirect, request

from utils.url import URL
from utils.files import join

from .elements import Button
from .taggers import DIV, SPAN, Tagger

# __all__ = ['Navitem', 'Navbar', 'Divider', 'Dropdown']
__all__ = ['Navitem', 'Navbar']

class Burger(Button):
    def __init__(self, name, **attributes):
        children = [SPAN(), SPAN(), SPAN()]
        attributes = dict(_role='button', **attributes)
        attributes["data-target"] = name
        attributes["aria-label"] = "menu"
        attributes["aria-expanded"] = "false"
        Button.__init__(self, *children, **attributes)
        self._class.replace('button', 'navbar-burger')

class Navitem(Button):
    def __init__(self, *children, **attributes):
        Button.__init__(self, *children, type='link', **attributes)
        self._class.replace('button', 'navbar-item icon-text is-tab')

    @property
    def activate(self):
        self._class += 'is-active'

    @property
    def desactivate(self):
        self._class -= 'is-active'

# class Divider(Tagger):
#     def __init__(self, *children, **attributes):
#         Tagger.__init__(self, *children, **attributes, _base='HR')
        # self._class += 'navbar-divider'

# class Dropdown(Navitem):
#     def __init__(self, title=None, *children, **attributes):
#         self.link = A(title, _class="navbar-link")
#         self.list = DIV(*children, _class="navbar-dropdown")
#         Navitem.__init__(self, self.link, self.list, **attributes)
#         self._class.replace('navbar-item icon-text', 'is-hoverable')
    
    # @property
    # def activate(self): 
    #     if activate(self.list.children):
    #         self.link._class += 'is-active'


class Navbar(Tagger):
    AUTORIZED_POSITIONS = ['top', 'bottom']
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
        self._class += self.__class__.__name__.lower()
        self._class += "is-fullhd"

    def __get_color__(self):
        return self.back_color
    def __set_color__(self, name):
        self.back_color = name
    def __del_color__(self):
        del self.back_color
    color = property(__get_color__, __set_color__, __del_color__)

    def __get_position__(self):
        for position in self.AUTORIZED_POSITIONS:
            if f'is-fixed-{position}' in self._class.list:
                return position
        return None
    def __set_position__(self, name):
        if name in self.AUTORIZED_POSITIONS:
            hold = self.__get_position__()
            self._class.replace(f'is-fixed-{hold}', f'is-fixed-{name}')
            for navitem in self.start.children+self.end.children:
                if isinstance(navitem, Navitem):
                    if 'has-dropdown' in navitem._class.list:
                        if name == 'top':
                            navitem._class -= 'has-dropdown-up'
                        else:
                            navitem._class += 'has-dropdown-up'
    position = property(__get_position__, __set_position__)

    @property
    def open(self):
        url = URL(request.full_path)
        del url.vars['navbar']
        self.burger['_href'] = url()
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
    def is_open(self):
        if "is-active" in self.menu._class.list:
            return True
        return False

    @property
    def activate(self):
        if request.args.get('navbar') == 'open':
            self.open
        else:
            self.close
        for navitem in self.start.children+self.end.children:
            url = URL(request.full_path)
            if len(url.args) >= 2:
                app_url = join(url.args[0], url.args[1])
                if app_url == navitem.url:
                    navitem.activate