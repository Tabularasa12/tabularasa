from flask import url_for
from .. import app
from utils.html import *
from utils.functions import labelize

@app.route('/')
@app.route('/index')
@app.to_page()
def index():
    body = A(
        Image(url=app.page.logo['_href'], replace="Logo", size=100),
        _href=url_for('index'),
        _title = labelize("recharger la page"),
    )
    return locals()
