from utils.html import *
from wtforms import StringField, validators

__all__ = ['Form_config']

# class Form_config(Form):
#     name = StringField(
#         "Nom d'utilisateur",
#         Validator_name
#     )
#     mail = StringField(
#         "Email",
#         Validator_email
#     )

class Form_config(metaclass=Html_form):
    fields = dict(
        name = dict(
            html = Field_name,
            flask = StringField,
            title = "nom d'utilisateur",
            validators = Validator_name
        ),
        mail = dict(
            html = Field_email,
            flask = StringField,
            title = 'email',
            validators = Validator_email
        )
    )
    title = 'configuration'