from importlib import import_module
from flask import Flask, Blueprint, Response, render_template, request, Markup, url_for
from flask.helpers import send_from_directory
from functools import wraps
from .icons import icons
from .bulma import bulma
from .functions import control_path_necessaries, labelize
from .files import *
from .html import *
from .regex import REGEX
from .parameters import Parameters, edict
from settings import *

NECESSARIES = dict(
    apps = 'apps',
    static = 'static',
    utils = 'utils',
    functions = join('utils', 'functions.py'),
    files = join('utils', 'files.py'),
    favicon = join('static', 'favicon.ico'),
    template = join('utils', 'html', DEFAUT_TEMPLATE),
    icons = join('utils', 'icons'),
    config = DEFAULT_CONFIG_FILE_NAME
)

def add_folder_route(app, name, path, download=False):
    rule = f'/{name}/<path:filename>'
    view_func = lambda filename: send_from_directory(path, filename, as_attachment=download)
    app.add_url_rule(rule, name, view_func=view_func)


class Master(Flask):
    def __init__(self, import_name, **attributes):
        Flask.__init__(self, import_name, **attributes)
        add_folder_route(self, 'apps', join(self.root_path, NECESSARIES['apps']))
        self.template_folder = dirname(NECESSARIES['template'])
        add_folder_route(self, 'css', dirname(bulma.path), download=DEFAULT_FILE_DOWNLOAD)
        add_folder_route(self, 'icons', join(self.root_path, NECESSARIES['icons']), download=DEFAULT_FILE_DOWNLOAD)

        if control_path_necessaries(self.root_path, NECESSARIES):
            pass
        
        self.add_url_rule('/update/<string:mode>', 'update', view_func=self.update, methods=["POST"])

        self.page_parameters = Parameters(defaults=NECESSARIES['config'])
        self.page_parameters['name'] = labelize(self.import_name)
        self.page_parameters['title'] = labelize(self.import_name)
        self.page = Page(self.page_parameters)
    
    def update(mode):
        mode = True if mode == 'true' or mode == 'True' else False
        if request.method == 'POST' and mode:
            subprocess.call(["git", "stash", "save"])
            subprocess.call(["git", "pull"])
        return dict()

    def _page(self):
        page = self.page
        page.bulma['_href'] = url_for('css', filename=bulma.css)
        page.icons['_href'] = url_for('icons', filename=icons.css)
        page.favicon['_href'] = url_for('static', filename=page.p.favicon)
        page.logo['_href'] = url_for('static', filename=page.p.logo)
        page.navbar.activate
        return page

    def to_page(self, template=DEFAUT_TEMPLATE):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                template_name = template
                if template_name is None:
                    template_name = f"{request.endpoint.replace('.', '/')}.html"
                ctx = f(*args, **kwargs)
                if ctx is None:
                    ctx = {}
                elif not isinstance(ctx, dict):
                    return ctx
                for k, v in ctx.items():
                    if isinstance(v, Tagger):
                        exec(f'self.page.{k}.update(v)')
                return render_template(DEFAUT_TEMPLATE, page=Markup(self.page))
            return decorated_function
        return decorator

    def import_apps(self, path):
        app_names = [app for app in listdir(path, type='dir', regex=REGEX['apps'])]
        path = path.strip(sep()).replace(sep(), '.')
        for a in app_names:
            app = import_module(f'{path}.{a}').app
            self.register_blueprint(app, url_prefix=f'/{a}')

    def controllers(self):
        apps = []
        for c in listdir(join(self.root_path, 'controllers'), type='file', regex=REGEX['controllers']):
            apps.append(f'{self.import_name}.controllers.{c}'.strip('.py'))
        return apps

class App(Blueprint):
    def __init__(self, name, import_name, master):
        Blueprint.__init__(self, name, import_name, url_prefix=join(sep(), name))
        self.master = master
        base_path = self.root_path.split(self.master.root_path)[1]
        self.static_folder = join(self.root_path, 'static')
        parameters_file = join(base_path.strip(sep()), DEFAULT_CONFIG_FILE_NAME)
        self.page_parameters = Parameters(defaults=parameters_file)
        self.page_parameters['name'] = labelize(self.name)
        self.page_parameters['title'] = f'{labelize(master.name)} -> {self.name}'
        self.page = Page(self.page_parameters)


    controllers = Master.controllers
    to_page = Master.to_page
    
    def _page(self):
        page = self.page
        page.bulma['_href'] = url_for('css', filename=bulma.css)
        page.icons['_href'] = url_for('icons', filename=icons.css)
        page.favicon['_href'] = url_for(f'{self.name}.static', filename=page.p.favicon)
        page.logo['_href'] = url_for(f'{self.name}.static', filename=page.p.logo)
        page.navbar.activate
        return page

