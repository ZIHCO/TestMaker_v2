#!/usr/bin/python3
"""this contains the exam class"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Exam(BaseModel, Base):
    """creates an exam"""
    if getenv('TESTMAKER_TYPE_STORAGE') == 'db':
        __tablename__ = 'exams'
        examiner_id = Column(String(60), ForeignKey('examiners.id'),
                             nullable=False)
        name = Column(String(128), nullable=False)
        total_point = Column(Integer, nullable=False, default=100)
        questions = relationship('Question', backref='exam')
        grades = relationship('Grade', backref='exam_grades')
    else:
        examiner_id = ""
        name = ""
        question_ids = []
        total_point = 0
    def __init__(self, *args, **kwargs):
        """initializes examiner"""
        super().__init__(*args, **kwargs)
