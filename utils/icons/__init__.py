from os.path import dirname, join
from .models import Icons

icons = Icons(join(dirname(__file__), 'ressources', 'css', 'all.css'))
