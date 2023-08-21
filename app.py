import subprocess
from importlib import import_module
from flask import request, url_for
#essai
from utils.apps import NECESSARIES, Master, App
from utils.bulma import bulma
from utils.icons import icons
from utils.files import *
from utils.functions import labelize
from utils.html import *
from utils.regex import REGEX
from utils.parameters import Parameters

# A essayer pour avoir plusieurs application valides l'une à côté de l'autre
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from frontend_app import application as frontend
# from backend_app import application as backend

# application = DispatcherMiddleware(frontend, {
#     '/backend': backend
# })

default = Master(basename(dirname(__file__)))

@default.before_request
def init_page():
    page = default._page()
    page.color = 'transparent'
    page._style += "background-image: linear-gradient(to right top, yellow, purple);"
    page.body._class += 'is-justify-content-center'
    page.burger.text_color = 'white'
    page.navbar.color = 'black'
    page.navbar.link.hide
    navbar_end = Navitem(Icon('cog', color='white'),_href=url_for('admin.index'))
    page.navbar.end.update(navbar_end)

@default.route('/update/<string:mode', methods=["POST"])
def update(mode):
    mode = True if mode == 'true' or mode == 'True' else False
    if mode:
        subprocess.call(["git", "pull"])
    return dict()

@default.route('/')
@default.route('/index')
@default.to_page()
def index():
    body = A(
        IMG(_src=url_for('static', filename='logo.png'), _alt="Logo", _style='margin-left:auto;margin-right:auto;max-width:300px;'),
        _href=url_for('index'),
        _title = labelize("recharger la page"),
    )
    return locals()

admin = App('admin', __name__, default)
for c in listdir('controllers', type='file', regex=REGEX['controllers']):
    import_module(f'controllers.{c}'.strip('.py')).admin

@admin.before_request
def init_page():
    page = admin._page()
    page.body._class += 'is-justify-content-center'

default.import_apps(NECESSARIES['apps'])

default.register_blueprint(admin)
print(default.url_map)
print(default.blueprints)