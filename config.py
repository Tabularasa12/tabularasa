from secrets import token_hex as secret_key

__all__ = ['Production', 'Development']

class Config(object):
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///default.sqlite3'
    SECRET_KEY = secret_key()
    MAIL_SERVER = 'smtp.free.fr'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'etienne.mousseau.12'
    MAIL_PASSWORD = 'signer10'
    HEADER = dict(
        autor = "Tabularasa",
        charset = "UTF-8",
        description = "Regarder le passé pour construire l'avenir",
        lang = "fr",
        viewport = "width=device-width, initial-scale=1",
    )
    PAGE = dict(
        color = "transparent",
        navbar = "top",
        height = "fullheight"
    )

class Production(Config):
    PREFERRED_URL_SCHEME = 'https'
    SERVER_NAME = 'tabularasa.pythonanywhere.com'
    APPLICATION_ROOT = '/'
    DB_CREATE_ALL = False

class Development(Config):
    PREFERRED_URL_SCHEME = ''
    SERVER_NAME = '127.0.0.1:5000'
    APPLICATION_ROOT = '/'
    DB_CREATE_ALL = True
