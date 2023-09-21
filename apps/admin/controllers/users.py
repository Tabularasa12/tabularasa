from flask import url_for
from .. import app
from utils.html import *
from utils.functions import labelize
from models import Users

@app.route('/users', methods=['GET', 'POST'])
@app.to_page()
def users():
    body = Users.query.all()
    return locals()

# body = Buttons(logo, _class='is-centered')
# users = Users.query.all()
# users_buttons = []
# for user in users:
#     users_buttons.append(Button(user.email, user.role))
# foot = Buttons(*users_buttons, _class='is-centered')