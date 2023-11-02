#!/usr/bin/python3
"""this class holds the question class"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey


class Option(BaseModel, Base):
    """structure question"""
    if getenv('TESTMAKER_TYPE_STORAGE') == 'db':
        __tablename__ = 'options'
        option = Column(String(1024), nullable=False)
        question_id = Column(String(60), ForeignKey('questions.id'), nullable=False)
