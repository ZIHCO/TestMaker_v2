#!/usr/bin/python3
"""this renders the home page"""
from website.v1.views import app_views
from flask import (render_template, request, flash,
                  redirect, url_for)
from werkzeug.security import generate_password_hash
from models import storage
from models.examiner import Examiner

@app_views.route('/signin', strict_slashes=False,
                 methods=['GET', 'POST'])
def sign_in():
    """render the home page"""
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        if request.form.get("password1") == request.form.get("password2"):
            password = generate_password_hash(request.form.get("password1"),
                                                               method='SHA256')
        else:
            flash("Passwords don\'t match.", category='error')
        last_name = request.form.get("last_name")

        if len(email) < 10:
            flash("Email must be greater than 9 characters.", category='error')
        elif len(first_name) < 3:
            flash("Email must be greater than 9 characters.", category='error')
        elif len(last_name) < 3:
            flash("Last name must be greater than 2 characters.", category='error')
        elif len(password) < 6:
            flash("Password must be greater than 5 characters.", category='error')
        else:
            new_dict = {
                       "email": email,
                       "password": password,
                       "last_name": last_name,
                       "first_name": first_name
                      }
            obj = Examiner(**new_dict)
            storage.new(obj)
            storage.save()
            flash("Account created! Login to continue.", category='success')
            return redirect(url_for('app_views.login'))
    return render_template("sign_in.html")
