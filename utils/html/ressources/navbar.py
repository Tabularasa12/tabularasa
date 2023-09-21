from flask import redirect, request

from utils.url import URL

from .elements import Button
from .taggers import DIV, SPAN, Tagger

# __all__ = ['Navitem', 'Navbar', 'Divider', 'Dropdown']
__all__ = ['Navitem', 'Navbar']

class Burger(Button):
    def __init__(self, name, **attributes):
        children = [SPAN(), SPAN(), SPAN()]
        attributes = dict(_role='button', _class="navbar-burger", **attributes)
        attributes["data-target"] = name
        attributes["aria-label"] = "menu"
        attributes["aria-expanded"] = "false"
        Button.__init__(self, *children, **attributes)
        self._class -= self.__class__.__name__.lower()

class Navitem(Button):
    def __init__(self, *children, **attributes):
        Button.__init__(self, *children, **attributes)
        self._class.replace(self.__class__.__name__.lower(), 'navbar-item icon-text')

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


AUTORIZED_POSITIONS = ['top', 'bottom']
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
    
    def __get_position__(self):
        for position in AUTORIZED_POSITIONS:
            if f'is-fixed-{position}' in self._class.list:
                return position
        return None
    def __set_position__(self, name):
        if name in AUTORIZED_POSITIONS:
            hold = self.__get_position__()
            self._class.replace(f'is-fixed-{hold}', f'is-fixed-{name}')
            if 'parent' in self.__dict__.keys():
                element = self.parent
                while element.name != 'HTML':
                    element = element.parent
                
                element._class.replace(f'has-navbar-fixed-{hold}', f'has-navbar-fixed-{name}')
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