from flask import url_for
from .. import app
from utils.html import *
from utils.icons import icons
from utils.functions import labelize

@app.route('/icon')
@app.to_page()
def icon():
    icon = []
    for name in sorted(icons.list.keys()):
        icon.append(Button(Icon(name), Text(name)))
    body = DIV(*icon)
    return dict(body=body)