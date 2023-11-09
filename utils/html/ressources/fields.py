from utils.html.ressources.form import *
from wtforms.validators import *
from wtforms import SelectField, RadioField
from utils.html.ressources.taggers import AUTORIZED_COLORS

__all__ = [
    'field_color',
    'field_navbar_top_bottom'
]

color_choices = [('chooze', 'Choisissez une couleur')]
for c in AUTORIZED_COLORS:
    color_choices.append((c, labelize(c)))
field_color = dict(
    html = Field_color,
    flask = SelectField(
        "Couleur",
        validators = [
            Required(message='Nécessaire'),
            NoneOf([color_choices[0][0]], message='Nécessaire')
        ],
        choices = color_choices
    ),
)
field_navbar_top_bottom = dict(
    html = Field_navbar_position,
    flask = RadioField(
        'position du menu',
        validators = [InputRequired(message='Nécessaire')],
        choices = [('top', 'haut'), ('bottom', 'bas')]
    )
)