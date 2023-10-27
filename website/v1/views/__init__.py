#!/usr/bin/python3
"""instantiate this package"""
from flask import Blueprint

app_views = Blueprint(name='app_views', import_name='__name__',
                      url_prefix='/')

if app_views is not None:
    from website.v1.views.index import *
    from website.v1.views.login import *
    from website.v1.views.sign_in import *
    from website.v1.views.dashboard import *
