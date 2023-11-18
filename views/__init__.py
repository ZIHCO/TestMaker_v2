#!/usr/bin/python3
"""instantiate this package"""
from flask import Blueprint
from models import storage
from models.examiner import Examiner
 
app_views = Blueprint(name='app_views', import_name='__name__',
                      url_prefix='/')

if app_views is not None:
    from views.index import *
    from views.login import *
    from views.sign_in import *
    from views.dashboard import *
    from views.make_new_test import *
    from views.add_new_question import *
