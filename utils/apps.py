from functools import wraps
from importlib import import_module
import json
import git
import hashlib
import hmac
import os
import datetime
from copy import deepcopy
from markupsafe import Markup
from flask import (
    Blueprint,
    Flask,
    Response,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app
)
from flask.helpers import send_from_directory
from settings import *

from .bulma import bulma
from .files import *
from .functions import control_path_necessaries, labelize, now
from .html import *
from .icons import icons
from .regex import REGEX
from .url import URL
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail
from utils.config import *
from wtforms import Form, StringField, validators

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

# mail = Mail()
db = SQLAlchemy()
from models import *

class Master(Flask):
    def __init__(self, import_name, **attributes):
        Flask.__init__(self, import_name, **attributes)
        add_folder_route(self, APPS_FOLDER_NAME, join(self.root_path, NECESSARIES['apps']))
        self.template_folder = dirname(NECESSARIES['template'])
        add_folder_route(self, 'css', dirname(bulma.path), download=DEFAULT_FILE_DOWNLOAD)
        add_folder_route(self, 'icons', join(self.root_path, NECESSARIES['icons']), download=DEFAULT_FILE_DOWNLOAD)
        self.name = labelize(import_name)
        self.title = labelize(import_name)
        run_mode = Development if self.config['DEBUG'] else Production 
        self.config.from_object(run_mode())
        self.page_config_file_path = join(self.root_path, DEFAULT_CONFIG_FILE_NAME)
        
        # mail.init_app(self)
        db.init_app(self)

        if control_path_necessaries(self.root_path, NECESSARIES):
            pass

        with self.app_context():
            if self.config['DB_CREATE_ALL']:
                db.create_all()
                if not Db_roles.query.all():
                    db.session.add(Db_roles(name='administrateur'))
                    db.session.add(Db_roles(name='utilisateur'))
                if not Db_users.query.all():
                    db.session.add(Db_users(email='email', password='password', active=True, confirmed_at=datetime.datetime.now(), role='administrateur'))
                db.session.commit()
            self.page = Masterpage(self)
            
            for c in self.controllers:
                import_module(c).default


        @self.route('/update', methods=['POST'])
        def update():
            if request.method == 'POST':
                
                def verify_signature(x_hub_signature, data, private_key):
                    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
                    algorithm = hashlib.__dict__.get(hash_algorithm)
                    encoded_key = bytes(private_key, 'latin-1')
                    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
                    return hmac.compare_digest(mac.hexdigest(), github_signature)

                key = os.environ.get('GIT_TOKEN')
                data = request.data
                signature = request.headers['X-Hub-Signature-256']
                if verify_signature(signature, data, key):
                    repo = git.Repo(join(self.root_path, '.git'))
                    origin = repo.remotes.origin
                    origin.pull()
                    return dict()
                else:
                    raise ValueError("Request signatures didn't match!")
            else:
                raise ValueError("Wrong event type")

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
                    if self.page.get_children_by_id(k):
                        if isinstance(v, (Tagger, int, str)):
                            exec(f'self.page.{k}.update(v)')
                        if isinstance(v, (list, tuple)):
                            exec(f'self.page.{k}.update(*v)')
                        if isinstance(v, (dict)):
                            exec(f'self.page.{k}.update(**v)')
                return render_template(DEFAUT_TEMPLATE, page=Markup(self.page))
            return decorated_function
        return decorator

    def import_apps(self, path):
        app_names = [app for app in listdir(path, type='dir', regex=REGEX['apps'])]
        for a in app_names:
            import_name = join(path,a).replace(sep(), '.')
            app = import_module(import_name).app
            self.register_blueprint(app, url_prefix=f'/{a}')
            with self.app_context():
                for app in self.blueprints.values():
                    app.page.favicon['_href'] = url_for(f'{app.name}.static', filename=DEFAULT_FAVICON_FILE_NAME)
                    app.page.logo['_href'] = url_for(f'{app.name}.static', filename=DEFAULT_LOGO_FILE_NAME)

    @property
    def controllers(self):
        apps = []
        for c in listdir(join(self.root_path, 'controllers'), type='file', regex=REGEX['controllers']):
            apps.append(f'{self.import_name}.controllers.{c}'.strip('.py'))
        return apps

class App(Blueprint):
    def __init__(self, name, import_name, master):
        Blueprint.__init__(self, name, import_name, url_prefix=join(sep(), name), static_folder='static')
        self.master = master
        self.title = labelize(self.name)
        self.config = deepcopy(master.config)
        self.page_config_file_path = join(self.root_path, DEFAULT_CONFIG_FILE_NAME)

        with self.master.app_context():
            self.page = Apppage(self)

        @self.route('/config', methods=['GET', 'POST'])
        @self.to_page()
        def config():
            print(request.form)
            body = Html_form(Form_config, request)

            # body = Form_config(request)
            # body = FORM(
            #     DIV(
            #         LABEL('Email', _class='label'),
            #         DIV(
            #             INPUT(_class='input is-danger', _type='email', _placeholder="Email input", _value="hello@"),
            #             SPAN(I(_class="fas fa-envelope"), _class='icon is-small is-left'),
            #             SPAN(I(_class="fas fa-exclamation-triangle"), _class='icon is-small is-right'),
            #             P('This email is invalid', _class='help is-danger'),
            #             _class='control has-icons-left has-icons-right'
            #         ),
            #         _class='field'
            #     ),
            #     _class='form box'
            # )
            
            return locals()


    controllers = Master.controllers
    to_page = Master.to_page


