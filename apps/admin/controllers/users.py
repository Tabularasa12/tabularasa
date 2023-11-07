from flask import url_for
from .. import app
from utils.html import *
from utils.functions import labelize
from models import Db_users

@app.route('/users')
@app.to_page()
def users():
    body = Db_users.query.all()
    return locals()

# body = Buttons(logo, _class='is-centered')
# users = Users.query.all()
# users_buttons = []
# for user in users:
#     users_buttons.append(Button(user.email, user.role))
# foot = Buttons(*users_buttons, _class='is-centered')