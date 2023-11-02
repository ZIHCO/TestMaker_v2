#!/usr/bin/python3
"""The examinee module"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Examinee(BaseModel, Base, UserMixin):
    """the examinee"""

    if getenv('TESTMAKER_TYPE_STORAGE') == 'db':
        __tablename__ = 'examinees'
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        examiner_id = Column(String(60), ForeignKey('examiners.id'),
                             nullable=False)
        exam_id = Column(String(60), ForeignKey('exams.id'),
                             nullable=False)
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
    else:
        first_name = ""
        last_name = ""
        password = ""
        exam_id = ""
        role = ""
