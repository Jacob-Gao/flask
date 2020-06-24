from flask import Blueprint

app01 = Blueprint(
    'app01',
    __name__,
    template_folder='templates',

)

from .views.initial_ecs import *
from .views.get_log import *
from  .views.install_zabbix import *
from  .views.vpn import *
