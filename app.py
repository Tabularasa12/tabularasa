#essai2
import requests
import secrets
import subprocess
from importlib import import_module
# import pdfkit
from flask import request, url_for, redirect, session
# from utils.apps import NECESSARIES, Master, App, db, mail
from utils.apps import NECESSARIES, Master, App, db
from utils.bulma import bulma
from utils.icons import icons
from utils.files import *
from utils.url import URL
from utils.functions import labelize, now
from utils.html import *
from utils.regex import REGEX
from utils.json import json, Json
from settings import *
from models import *
import datetime
# from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail, Message

# A essayer pour avoir plusieurs application valides l'une à côté de l'autre
# from werkzeug.middleware.dispatcher import DispatcherMiddleware
# from frontend_app import application as frontend
# from backend_app import application as backend

# application = DispatcherMiddleware(frontend, {
#     '/backend': backend
# })

def create_app():
    default = Master(basename(dirname(__file__)))
    default.page._style += "background-image: linear-gradient(to right top, yellow, purple);"
    default.page.body._class += 'is-justify-content-center'

    @default.route('/')
    @default.route('/index')
    @default.to_page()
    def index():
        logo = A(
            IMG(_src=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), _alt="Logo", _style='max-width:300px;'),
            _href=url_for('index'),
            _title = labelize("recharger la page"),
        )

        default.page.color = 'transparent'
        # apps = [Button(app.name, _href=url_for(f'{app.name}.index'), color=app.page.color) for app in default.blueprints.values() if app.name != 'admin']
        # body = [Buttons(logo, _class='is-centered'), Buttons(*apps, _class='is-centered')]
        body = Buttons(logo, _class='is-centered')
        users = Users.query.all()
        users_buttons = []
        for user in users:
            users_buttons.append(Button(user.email, user.role))
        foot = Buttons(*users_buttons, _class='is-centered')

        

        # msg = Message("Hello",
        #     sender = 'locauxmotives@gmail.com',
        #     recipients=['etienne@semou.fr'],
        #     body = 'ok, merci',
        #     html = default.page.content.xml(),
        # )
        # options = {
        #     # 'page-size': 'A4',
        #     # 'dpi': 100,
        #     # 'orientation' : 'Portrait',
        #     # 'disable-smart-shrinking': True,
        #     # 'page-height' : 300,
        #     # 'page-width' : 300,
        # }
        # pdfkit.from_url('http://127.0.0.1:5000/pdf', 'static/out.pdf', options=options)
        # # with default.open_resource(url_for('static', filename='out.pdf')) as fp:
        # #     msg.attach(url_for('static', filename='out.pdf'), "file/pdf", fp.read())

        # # mail.send(msg)
        return locals()
    
    # @default.route('/pdf')
    # @default.to_page()
    # def pdf():
    #     logo = A(
    #         IMG(_src=url_for('static', filename=DEFAULT_LOGO_FILE_NAME), _alt="Logo", _style='max-width:300px;'),
    #         _href=url_for('index'),
    #         _title = labelize("recharger la page"),
    #     )
    #     body = Buttons(logo, _class='is-centered')
    #     return locals()

    # admin = App('admin', __name__, default)
    # for c in listdir('controllers', type='file', regex=REGEX['controllers']):
    #     import_module(f'controllers.{c}'.strip('.py')).admin

    # @admin.before_request
    # def init_page():
    #     page = admin._page()
    #     page.body._class += 'is-justify-content-center'

    # default.import_apps(NECESSARIES['apps'])

    # default.register_blueprint(admin)
    # print(default.url_map)
    # print(default.blueprints)


    @default.route('/create_user/<string:email>/<string:password>', methods=['GET', 'POST'])
    def create_user(email, password):
        db.session.add(Users(email=email, password=password, active=True, confirmed_at=datetime.datetime.now(), role='utilisateur'))
        db.session.commit()
        return redirect(url_for('index'))

    return default