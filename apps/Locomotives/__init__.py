from flask import url_for
from importlib import import_module
from utils.apps import App
from app import default, admin
from settings import DEFAUT_TEMPLATE, DEFAULT_CONFIG_FILE_NAME
from utils.files import *
from utils.html import *
from utils.json import Json
from utils.parameters import Parameters

config = Json(join(dirname(__file__), DEFAULT_CONFIG_FILE_NAME))
print(config.datas)
app_name = config['name']
app = App(app_name, __name__, default)

@app.before_request
def init_page():
    page = app._page()
    page._class += 'has-navbar-fixed-top'
    page.body._class += 'is-justify-content-center'
    navbar = Navbar(_id='navbar', _class='is-fixed-top')
    navbar.burger.text_color = 'white'
    navbar_end = Navitem(Icon('cog', color='white'),_href=url_for(f'{admin.name}.index'))
    navbar.end.update(navbar_end)
    navbar.color = page.color
    navbar.activate
    page.head.update(navbar)

for c in app.controllers():
    import_module(c).app

