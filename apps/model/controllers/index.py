from flask import url_for
from .. import app
from utils.html import *
from utils.functions import labelize

@app.route('/')
@app.route('/index')
@app.to_page()
def index():
    body = Title(app.page.p.name)
    return locals()
