#!/usr/bin/python3
"""instantiate this package"""
from flask import Blueprint
from models import storage
from models.examiner import Examiner
 
app_views = Blueprint(name='app_views', import_name='__name__',
                      url_prefix='/')

if app_views is not None:
    from website.v1.views.index import *
    from website.v1.views.login import *
    from website.v1.views.sign_in import *
    from website.v1.views.dashboard import *
    from website.v1.views.make_new_test import *
    from website.v1.views.add_new_question import *
