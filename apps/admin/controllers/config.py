from flask import redirect, url_for, request
from .. import app
from utils.html import *
from ..models import Form_config
from utils.functions import labelize

@app.route('/config', methods=['GET', 'POST'])
@app.to_page()
def config():
    body = Form_config(app.page, request)
    if body.validate:
        values = body.values
        app.page.color = values['color']
        app.page.config['color'] = values['color']
        app.page.navbar.position = values['navbar']
        app.page.config['navbar']['position'] = values['navbar']
    return locals()
