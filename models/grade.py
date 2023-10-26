#!/usr/bin/python3
"""grades class module"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, ForeignKey


class Grade(BaseModel, Base):
    """keep records"""
    if getenv('TESTMAKER_TYPE_STORAGE') == 'db':
        __tablename__ = 'grades'
        exam_id = Column(String(60), ForeignKey('exams.id'), nullable=False)
        examiner_id = Column(String(60), ForeignKey('examiners.id'), nullable=False)
        score = Column(Integer, nullable=False, default=0)
        examinee_id = Column(String(60), ForeignKey('examinees.id'), nullable=False)
    else:
        exam_id = ""
        examiner_id = ""
        examinee_id = ""
        score = 0
