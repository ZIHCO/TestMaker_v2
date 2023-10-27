#!/usr/bin/python3
"""this renders the home page"""
from website.v1.views import app_views
from flask import render_template

@app_views.route('/<text>', strict_slashes=False)
def dashboard(text):
    """render the home page"""
    return render_template("dashboard.html", name=text)
