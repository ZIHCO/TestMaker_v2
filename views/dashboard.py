#!/usr/bin/python3
"""this renders the examiner dashboard"""
from views import app_views
from flask import render_template
from flask_login import current_user, login_required

@app_views.route('/<text>', strict_slashes=False)
@login_required
def dashboard(text):
    """renders the examiner dashboard"""
    if (current_user.first_name + " " + current_user.last_name ==
        text.replace("_", " ")):
        name = current_user.first_name + " " + current_user.last_name
        return render_template("dashboard.html", name=name)
