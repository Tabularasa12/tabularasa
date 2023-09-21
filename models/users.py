from utils.apps import db

def __str__(model):
    response = dict()
    for n, e in model.__dict__.items():
        response[n] = e
    return str(response)
            

class Roles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    users = db.relationship('Users', backref='roles')

    def __repr__(self):
        return str(self.__dict__)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    role = db.Column(db.String(80), db.ForeignKey('roles.name'))

    def __repr__(self):
        return str(self.__dict__)
