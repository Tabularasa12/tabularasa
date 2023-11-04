from utils.apps import db

__all__ = ['Db_roles', 'Db_users']

# def __str__(model):
#     response = dict()
#     for n, e in model.__dict__.items():
#         response[n] = e
#     return str(response)


class Db_roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('Db_users', backref='Db_roles')

    def __repr__(self):
        return str(self.__dict__)

class Db_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    role = db.Column(db.String(80), db.ForeignKey('db_roles.name'))

    def __repr__(self):
        return str(self.__dict__)
