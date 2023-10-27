#!/usr/bin/python3
"""this renders the home page"""
from website.v1.views import app_views
from flask import render_template

@app_views.route('/', strict_slashes=False)
def home():
    """render the home page"""
    return render_template("home.html")
