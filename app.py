#!/usr/bin/python3
"""This is the app module"""
from flask import Flask
from models import storage
from views import app_views
from os import getenv
from models.engine.db_storage import conn
from flask_login import LoginManager
from models.examiner import Examiner
from models.examinee import Examinee


app = Flask(__name__)
app.config['SECRET_KEY'] = 'aseiop4567'

login_manager = LoginManager()
login_manager.login_view = 'app_views.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_examiner(id):
    if storage.get(Examiner, id):
        return storage.get(Examiner, id)
    elif storage.get(Examinee, id):
        return storage.get(Examinee, id)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """closes a session"""
    storage.close()


if __name__ == "__main__":
    if getenv('TESTMAKER_HOST') and getenv('TESTMAKER_PORT'):
        app.run(host=getenv('TESTMAKER_HOST'), port=getenv('TESTMAKER_PORT'),
                threaded=True)
