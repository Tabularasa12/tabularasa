from app import admin
from utils.html import *
from flask import url_for
from utils.functions import labelize

@admin.route('/')
@admin.route('/index')
@admin.to_page()
def index():
    body = A(
        IMG(_src=url_for(f'{admin.name}.static', filename='logo.png'), _alt="Logo", _style='margin-left:auto;margin-right:auto;max-width:300px;'),
        _href=url_for('index'),
        _title = labelize("recharger la page"),
    )
    return locals()
