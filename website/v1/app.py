#!/usr/bin/python3
"""This is the app module"""
from flask import Flask
from models import storage
from website.v1.views import app_views
from os import getenv
from models.engine.db_storage import conn
from flask_login import LoginManager
from models.examiner import Examiner


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Peace(1)wq'

login_manager = LoginManager()
login_manager.login_view = 'app_views.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_examiner(id):
    return storage.get(Examiner, id)

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(self):
    """closes a session"""
    storage.close()


if __name__ == "__main__":
    if getenv('TESTMAKER_HOST') and getenv('TESTMAKER_PORT'):
        app.run(host=getenv('TESTMKER_HOST'), port=getenv('TESTMAKER_PORT'),
                threaded=True)
