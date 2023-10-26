#!/usr/bin/python3
"""this class holds the question class"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, ForeignKey


class Question(BaseModel, Base):
    """structure question"""
    if getenv('TESTMAKER_TYPE_STORAGE') == 'db':
        __tablename__ = 'questions'
        question = Column(String(1024), nullable=False)
        answer = Column(String(128), nullable=False)
        point = Column(Integer, nullable=False, default=0)
        exam_id = Column(String(60), ForeignKey('exams.id'), nullable=False)
        examiner_id = Column(String(60), ForeignKey('examiners.id'), nullable=False)
    else:
        question = ""
        answer = ""
        incorrect = []
        exam_id = ""
        point = 0
