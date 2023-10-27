#!/usr/bin/python3
"""this renders the home page"""
from website.v1.views import app_views
from flask import (render_template, request, redirect,
        flash, url_for)
from models import storage
from models.examiner import Examiner
from werkzeug.security import check_password_hash

@app_views.route('/login', strict_slashes=False,
                 methods=['GET', 'POST'])
def login():
    """render the home page"""
    if request.method == "POST":
        password = request.form.get('password')
        email = request.form.get('email')
        examiners = storage.all(Examiner)
        for examiner_id, examiner in examiners.items():
            if (examiners[examiner_id].email == email and
                check_password_hash(examiners[examiner_id].password, password)):
                last_name = examiners[examiner_id].last_name
                first_name = examiners[examiner_id].first_name
                return redirect(url_for('app_views.dashboard',
                                **{"text": first_name + "_" + last_name}))
        flash("Incorrect password or email address.", category='error')
    return render_template("login.html")

@app_views.route('/logout', strict_slashes=False)
def logout():
    """end a session and return to the homepage"""
    return render_template("home.html")
