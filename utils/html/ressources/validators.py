
from wtforms import validators

__all__ = [
    'Validator_name',
    'Validator_email'
]

Validator_name = [
    validators.required(message='nécessaire'),
    validators.Length(min=4, message='trop court !!! (minmum 4 caractères)'),
    validators.Length(max=25, message="trop long !!! (maximum 25 caractères)"),
    validators.Regexp(r'^[a-z]{4,25}$', message='contient des caractères invalides')
]
Validator_email = [
    validators.required(message='nécessaire'),
    validators.email(message="Ceci n'est pas une adresse email valide")
]
