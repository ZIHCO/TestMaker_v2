#!/usr/bin/python3
"""this renders the home page"""
from website.v1.views import app_views
from flask import render_template
from flask_login import current_user, login_required

@app_views.route('/<text>', strict_slashes=False)
@login_required
def dashboard(text):
    """render the home page"""
    if (current_user.first_name + " " + current_user.last_name ==
        text.replace("_", " ")):
        name = current_user.first_name + " " + current_user.last_name
        return render_template("dashboard.html", name=name)
