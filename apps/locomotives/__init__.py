# from flask import url_for
# from settings import DEFAUT_TEMPLATE, DEFAULT_CONFIG_FILE_NAME
# from utils.html import *
from importlib import import_module
from utils.apps import App
from app import default
from utils.files import basename, dirname
app_name = basename(dirname(__file__))

app = App(app_name, __name__, default)


# @app.before_request
# def init_page():
#     page = app._page()
#     page._class += 'has-navbar-fixed-top'
#     page.body._class += 'is-justify-content-center'
#     navbar = Navbar(_id='navbar', _class='is-fixed-top')
#     navbar.burger.text_color = 'white'
#     navbar_end = Navitem(Icon('cog', color='white'),_href=url_for(f'{admin.name}.index'))
#     navbar.end.update(navbar_end)
#     navbar.color = page.color
#     navbar.activate
#     page.head.update(navbar)

for c in app.controllers:
    import_module(c).app

