#!/usr/bin/python3
"""this module contains the make_new_test definition
and my_tests definition"""
from views import app_views
from flask import (render_template, request, flash, redirect,
                   url_for)
from flask_login import current_user, login_required
from models.exam import Exam
from models import storage

@app_views.route('/<text>/make_new_test', strict_slashes=False,
                 methods=["GET", "POST"])
@login_required
def make_new_test(text):
    """render the make new test page"""
    examiner_name = current_user.first_name + " " + current_user.last_name
    if request.method == "POST":
        name = request.form.get('name')
        total_point = request.form.get('grade')
        if len(name) < 3:
            flash("Name cannot be less than 3 characters", category="error")
        else:
            new_dict = {
                        "name": name,
                        "total_point": total_point,
                        "examiner_id": current_user.id
                       }
            exams = storage.all(Exam)
            for exam_id, exam in exams.items():
                if exam.name == name and exam.examiner_id == current_user.id:
                    flash("Test already exists. Add a question to update "
                          "test.", category="error")
                    break
            else:
                obj = Exam(**new_dict)
                storage.new(obj)
                storage.save()
                flash("Examination created! Add questions to update examination.",
                  category="success")
            return redirect(url_for("app_views.add_new_question", **{"name": examiner_name.replace(" ", "_"), "exam_name": name.replace(" ", "_")}))
    return render_template("make_new_test.html",
                           name=examiner_name)

@app_views.route('/<text>/my_tests', strict_slashes=False)
@login_required
def my_tests(text):
    """renders the tests of login_examiner"""
    if (current_user.first_name + " " + current_user.last_name ==
        text.replace("_", " ")):
        exams = current_user.exams
        return render_template("my_tests.html", exams=exams, name=text)

@app_views.route('/<text>/my_tests/<exam_name>', strict_slashes=False)
@login_required
def this_tests(text, exam_name):
    """displays the questions of an exam"""
    exams = current_user.exams
    for exam in exams:
        if exam_name.replace("_", " ") == exam.name:
            return render_template("this_test.html", exam=exam, name=text, exam_name=exam_name)

@app_views.route('/<text>/my_candidates', strict_slashes=False)
@login_required
def my_candidates(text):
    """renders the tests of login_examiner"""
    if (current_user.first_name + " " + current_user.last_name ==
        text.replace("_", " ")):
        examinees = current_user.examinees
        return render_template("my_candidates.html", examinees=examinees, name=text, exams=current_user.exams, examiner=current_user)
