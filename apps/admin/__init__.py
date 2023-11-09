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
