from flask import url_for
from importlib import import_module
from utils.apps import App
from app import default
from utils.files import basename, dirname
from utils.html import *
from utils.functions import labelize
from settings import DEFAULT_LOGO_FILE_NAME

app_name = basename(dirname(__file__))

app = App(app_name, __name__, default)
for c in app.controllers:
    import_module(c).app

# @app.before_request
# def init():
#     app.page.navbar.end.append(Navitem(Icon('object-group'), url=url_for(f'{app.name}.icon')))
#     app.page._class += 'has-navbar-fixed-top'
#     app.page.body._class += 'is-justify-content-center'
    
#     navbar = Navbar(_id='navbar', _class='is-fixed-top')
    
#     navbar.link.update(IMG(_src=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), size=5, _title="Retour à la page d'accueil"), _href=url_for('index'))
    
#     navbar.burger.text_color = 'white'
    
#     start = []
#     for c in app.controllers:
#         c_name = c.rsplit('.', 1)[1]
#         if c_name != 'index':
#             start.append(Navitem(labelize(c_name), _href=url_for(f'{app.name}.{c_name}')))
#     navbar.start.update(*start)

#     admin = default.blueprints['admin']
#     end = Navitem(Icon('cog', color='white'), _href=url_for(f'{admin.name}.index'))
#     navbar.end.update(end)
#     navbar.color = app.page.color
#     navbar.activate
#     app.page.head.update(navbar)


