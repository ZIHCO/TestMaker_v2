#!/usr/bin/python3
"""this renders the home page"""
from flask import (render_template, request, redirect,
                   flash, url_for)
from models.examiner import Examiner
from models.examinee import Examinee
from models.exam import Exam
from models.question import Question
from models.grade import Grade
from models import storage
from werkzeug.security import check_password_hash
from views import app_views
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

@app_views.route('/take_test', strict_slashes=False,
                 methods=['GET', 'POST'])
def take_test():
    """renders the login for student"""
    if request.method == "POST":
        password = request.form.get('password')
        email = request.form.get('email')
        examinees = storage.all(Examinee)
        for examinee_id, examinee in examinees.items():
            if (examinees[examinee_id].email == email and
                check_password_hash(examinees[examinee_id].password,
                                    password)):
                login_user(examinee, remember=True)
                value = {"text": (current_user.first_name
                                  + "_" + current_user.last_name)}
                exam_name = request.form.get("exam_name")
                return redirect(url_for('app_views.test',
                                        exam_name=exam_name.replace(" ", "_"),
                                        examinee_name=examinee.first_name))
        flash("Incorrect password or email address.", category='error')

    return render_template("take_test.html")


@app_views.route('/<examinee_name>/<exam_name>/test', strict_slashes=False,
                 methods=['GET', 'POST'])
@login_required
def test(exam_name, examinee_name):
    examinee= current_user
    exams = storage.all(Exam)
    if request.method == "POST":
        score = 0
        for key, value in request.form.items():
            question = storage.get(Question, key)
            if value.replace("_", " ") == question.answer:
                score += question.point
        new_dict = {
                    "exam_id": current_user.exam_id,
                    "examiner_id": current_user.examiner_id,
                    "score": score,
                    "examinee_id": current_user.id
                    }
        grade_obj = Grade(**new_dict)
        storage.new(grade_obj)
        storage.save()
        logout_user()
        for exam_id, exam in exams.items():
            if exam.name == exam_name.replace("_", " "):
                exam_total_point = exam.total_point
                break
        flash(f"You have successfully submitted. You score {score} out of {exam_total_point}!",
              category="success")
        return redirect(url_for("app_views.home"))
    else:
        for exam_id, exam in exams.items():
            if exam.name == exam_name.replace("_", " "):
                return render_template("test.html", exam=exam, examinee=examinee)
