from flask import redirect, url_for, request
from .. import app
from utils.html import *
from models import Form_config
from utils.functions import labelize

@app.route('/config', methods=['GET', 'POST'])
@app.to_page()
def config():
    body = Form_config(request)
    if body.validate:
        print(body.values)
        return redirect(url_for('admin.index'))
    return locals()
