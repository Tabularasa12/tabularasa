from utils.files import basename, dirname

APP_NAME = basename(dirname(__file__))
DEFAUT_TEMPLATE = 'index.html'
DEFAULT_CONFIG_FILE_NAME = 'config.cfg'
DEFAULT_FAVICON_FILE_NAME = 'favicon.ico'
DEFAULT_LOGO_FILE_NAME = 'logo.png'
DEFAULT_FILE_DOWNLOAD = False
DEFAULT_LOG_FILE = 'logs.json'
DEFAULT_LOG_TIME_FORMAT = "%d-%m-%Y %H:%M:%S:%f"
APPS_FOLDER_NAME = 'apps'
DEFAULT_SIZE = 6