#!/usr/bin/python3
"""this renders the home page"""
from flask import (render_template, request, redirect,
                   flash, url_for)
from models.examiner import Examiner
from models import storage
from werkzeug.security import check_password_hash
from website.v1.views import app_views
from flask_login import (login_user, login_required, logout_user,
                         current_user)


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
                check_password_hash(examiners[examiner_id].password,
                                    password)):
                login_user(examiner, remember=True)
                value = {"text": (current_user.first_name
                                  + "_" + current_user.last_name)}
                return redirect(url_for('app_views.dashboard',
                                        **value))
        flash("Incorrect password or email address.", category='error')
    return render_template("login.html")


@app_views.route('/logout', strict_slashes=False)
@login_required
def logout():
    """end a session and return to the homepage"""
    logout_user()
    return redirect(url_for("app_views.home"))
