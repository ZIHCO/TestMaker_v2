#!/usr/bin/python3
"""this renders the home page"""
from views import app_views
from flask import (render_template, request, flash,
                  redirect, url_for)
from werkzeug.security import generate_password_hash
from models import storage
from models.examinee import Examinee
from models.examiner import Examiner
from flask_login import current_user, login_required

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
            return render_template("sign_in.html")
        last_name = request.form.get("last_name")

        if len(email) < 10:
            flash("Email must be greater than 9 characters.", category='error')
            return render_template("sign_in.html")
        elif len(first_name) < 3:
            flash("Email must be greater than 9 characters.", category='error')
            return render_template("sign_in.html")
        elif len(last_name) < 3:
            flash("Last name must be greater than 2 characters.", category='error')
            return render_template("sign_in.html")
        elif len(password) < 6:
            flash("Password must be greater than 5 characters.", category='error')
            return render_template("sign_in.html")
        else:
            new_dict = {
                        "email": email,
                        "password": password,
                        "last_name": last_name,
                        "first_name": first_name
                       }
            obj = Examiner(**new_dict)
            examiners = storage.all(Examiner)
            for examiner_id, examiner in examiners.items():
                if (examiners[examiner_id].email == email):
                    flash('Email already exists. Sign in with another email address',
                          category='error')
                    return render_template("sign_in.html")
                else:
                    storage.new(obj)
                    storage.save()
                    flash("Account created! Login to continue.", category='success')
                    return redirect(url_for('app_views.login'))
            else:
                storage.new(obj)
                storage.save()
                flash("Account created! Login to continue.", category='success')
                return redirect(url_for('app_views.login'))
    return render_template("sign_in.html")


@app_views.route("/<text>/add_candidate", strict_slashes=False,
                 methods=['GET', 'POST'])
@login_required
def add_candidate(text):
    """allow examiner to add candidates"""
    if (current_user.first_name + " " + current_user.last_name ==
        text.replace("_", " ")) and request.method == "GET":
        return render_template("add_candidate.html", name=text)
    elif request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
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
                        "first_name": first_name,
                        "examiner_id": current_user.id
                       }
            exams = current_user.exams
            for exam in exams:
                if exam.name == request.form.get("exam_name"):
                    exam_id = exam.id
                    break
            new_dict["exam_id"] = exam_id
            examinee_obj = Examinee(**new_dict)
            storage.new(examinee_obj)
            storage.save()
            flash(f"{new_dict['first_name']} {new_dict['last_name']} "
                  f"added successfully!", category="success")
            return render_template("add_candidate.html", name=text)
