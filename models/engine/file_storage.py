#!/usr/bin/python3
"""this module contains the FileStorage class"""
from models.base_model import BaseModel
from models.exam import Exam
from models.examiner import Examiner
from models.examinee import Examinee
from models.grade import Grade
from models.question import Question
import json
from os import path


class FileStorage:
    """this class serialises and dumps to a file the dictionary
    representation of an object and loads from a file the json
    representation of an object and deserialises back to the
    dictionary"""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if not cls:
            return FileStorage.__objects
        cls_objs = {}
        for key, value in FileStorage.__objects.items():
            if cls == value.__class__:
                cls_objs[key] = value
        return cls_objs

    def new(self, obj):
        """sets attribute to __objects with key as
        <obj class name>.id"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            FileStorage.__objects[key] = obj

    def save(self):
        """serialise __objects to JSON file"""
        json_dict = {}
        for key in self.__objects:
            json_dict[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(json_dict, f)

    def reload(self):
        """deserialises the json file to __objects"""
        if path.exists(self.__file_path):
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                obj_dict = json.load(f)
            for key, val in obj_dict.items():
                FileStorage.__objects[key] = eval(val['__class__'])(**val)

    def delete(self, obj=None):
        """delete obj from __objects"""
        if obj:
            key = obj.__class__.__name__ + "." + obj.id
            if key in FileStorage.__objects:
                del FileStorage.__objects[key]
