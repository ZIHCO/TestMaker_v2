#!/usr/bin/python3
"""This module contains the examiner class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Examiner(BaseModel, Base, UserMixin):
    """This class create an examiner"""

    if getenv('TESTMAKER_TYPE_STORAGE') == 'db':
        __tablename__ = 'examiners'
        last_name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        exams = relationship('Exam', backref='examiner')
        questions = relationship('Question',
                                 backref='examiner_questions')
        examinees = relationship('Examinee',
                                 backref='examiner_examinees')
        grades = relationship('Grade',
                              backref='examiner_grades')
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
    def __init__(self, *args, **kwargs):
        """initializes examiner"""
        super().__init__(*args, **kwargs)
