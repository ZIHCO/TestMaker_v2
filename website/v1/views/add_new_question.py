#!/usr/bin/python3
"""this renders the home page"""
from website.v1.views import app_views
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from models.exam import Exam
from models.question import Question
from models.option import Option
from models import storage

@app_views.route('/<name>/<exam_name>/add_new_question', strict_slashes=False,
                 methods=["GET", "POST"])
@login_required
def add_new_question(name, exam_name):
    """render the """
    if request.method == "POST":
        if request.form.get("multichoice") == "on":
            return redirect(url_for("app_views.add_multichoice",
                                    name=name, exam_name=exam_name))
    return render_template("add_new_question.html",
            **{"name": name, "exam_name": exam_name})


@app_views.route('/<name>/<exam_name>/add_new_question/add_multichoice',
                 strict_slashes=False, methods=["GET", "POST"])
@login_required
def add_multichoice(name, exam_name):
    """multichoice question maker"""
    if request.method == "POST":
        new_question = {"question": request.form.get("question"),
                        "point": request.form.get("point"),
                        "question_type": "multichoice",
                        "answer": request.form.get("answer"),
                        "examiner_id": current_user.id
                        }
        exams_of_current_user = current_user.exams
        for item in exams_of_current_user:
            if item.name == exam_name.replace("_", " "):
                exam_id = item.id
        new_question["exam_id"] = exam_id
        question_obj = Question(**new_question)
        storage.new(question_obj)
        storage.save()
        list_options = [request.form.get("answer"),
                        request.form.get("incorrect_answer1"),
                        request.form.get("incorrect_answer2"),
                        request.form.get("incorrect_answer3")]
        for item in list_options:
            new_option = {"question_id": question_obj.id,
                          "option": item}
            option_obj = Option(**new_option)
            storage.new(option_obj)
            storage.save()
        flash(f"Question add to {exam_name.replace('_', ' ')}")
        return redirect(url_for("app_views.add_new_question",
                **{"name": name, "exam_name": exam_name}))
    return render_template("add_multichoice.html", name=name, exam_name=exam_name)
