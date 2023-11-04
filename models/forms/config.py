from utils.html import *
from wtforms import StringField, validators

__all__ = ['Form_config']

class Form_config(Form):
    name = StringField(
        "Nom d'utilisateur",
        Validator_name
    )
    mail = StringField(
        "Email",
        Validator_email
    )