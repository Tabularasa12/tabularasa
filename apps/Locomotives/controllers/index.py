from flask import url_for
from .. import app
from utils.html import *
from utils.functions import labelize

@app.route('/')
@app.route('/index')
@app.to_page()
def index():
    body = A(
        IMG(_src=app.page.logo['_href'], _alt="Logo", _style='margin-left:auto;margin-right:auto;max-width:300px;'),
        _href=url_for('index'),
        _title = labelize("recharger la page"),
    )
    return locals()
