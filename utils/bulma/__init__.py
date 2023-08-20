from os.path import dirname, join
from .models import Bulma

bulma = Bulma(join(dirname(__file__), 'bulma.sass'))