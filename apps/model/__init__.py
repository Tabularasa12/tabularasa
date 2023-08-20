from flask import url_for
from importlib import import_module
from utils.apps import App
from app import default
from settings import DEFAUT_TEMPLATE, DEFAUT_CONFIG_FILE_NAME
from utils.files import *
from utils.html import *
from utils.parameters import Parameters

parameters_file = join(dirname(__file__).split(default.root_path)[1].lstrip(sep()), DEFAUT_CONFIG_FILE_NAME)
ADMIN_PARAMETERS = Parameters(defaults=parameters_file)

app = App(basename(dirname(__file__)), __name__, ADMIN_PARAMETERS, default)

@app.before_request
def init_page():
    page = app._page()
    page.color = 'link'
    page.body._class += 'is-justify-content-center'
    page.burger.text_color = 'white'
    page.navbar.link.hide()
    navbar_end = Navitem(Icon('cog', color='white'),_href=url_for('admin.index'))
    page.navbar.end.update(navbar_end)

for c in app.controllers():
    import_module(c).app

