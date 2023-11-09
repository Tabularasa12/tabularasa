from utils.html.ressources.form import *
from utils.html.ressources.fields import *
from wtforms import SelectField, RadioField
from utils.html.ressources.taggers import AUTORIZED_COLORS

__all__ = ['Form_config']

class Form_config(metaclass=Html_form):
    title = 'configuration'
    fields = dict(
        color = field_color,
        navbar = field_navbar_top_bottom
    )