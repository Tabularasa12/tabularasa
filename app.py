#essai2
import requests
import secrets
import subprocess
from importlib import import_module
# import pdfkit
from flask import request, url_for, redirect, session
from utils.apps import NECESSARIES, Master, App, db
from utils.bulma import bulma
from utils.icons import icons
from utils.files import *
from utils.url import URL
from utils.functions import labelize, now
from utils.html import *
from utils.regex import REGEX
from utils.json import json, Json
from settings import (
    APP_NAME,
    DEFAUT_TEMPLATE,
    DEFAULT_CONFIG_FILE_NAME,
    DEFAULT_FAVICON_FILE_NAME,
    DEFAULT_LOGO_FILE_NAME,
    DEFAULT_FILE_DOWNLOAD,
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_TIME_FORMAT,
    APPS_FOLDER_NAME
)
from models import *
import datetime

# A essayer pour avoir plusieurs application valides l'une à côté de l'autre
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from frontend_app import application as frontend
# from backend_app import application as backend

# application = DispatcherMiddleware(frontend, {
#     '/backend': backend
# })


default = Master(APP_NAME)
default.import_apps(NECESSARIES['apps'])
default.page._style += "background-image: linear-gradient(to right top, yellow, purple);"

@default.route('/')
@default.route('/index')
@default.to_page()
def index():
    head = Buttons(Button(Icon('cog'), url=url_for('admin.index'), color='primary', _class='is-outlined', _style='border:None'), _class='is-right')
    logo = A(
        Image(url=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), replace="Logo", size=300, text=labelize("recharger la page")),
        _href=url_for('index'),
    )

    apps = [Button(labelize(app.name), url=url_for(f'{app.name}.index'), color=app.page.color, ) for app in default.blueprints.values() if app.name != 'admin']
    body = Container(Buttons(logo, _class='is-centered'), Buttons(*apps, _class='is-centered'))

    return locals()



# print(default.url_map)
# print(default.blueprints)


