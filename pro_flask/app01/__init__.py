from flask import Blueprint

app01 = Blueprint(
    'app01',
    __name__,
    template_folder='templates',

)

from .views.views import *

