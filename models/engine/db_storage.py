#!/usr/bin/python3
"""Migrate storage to mysql server"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.examiner import Examiner
from models.exam import Exam
from models.examinee import Examinee
from models.grade import Grade
from models.question import Question

classes = {"Examiner": Examiner, "Exam": Exam, "Examinee": Examinee,
           "Question": Question, "Grade": Grade}

conn = (f"mysql+mysqldb://{getenv('TESTMAKER_MYSQL_USER')}"
        f":{getenv('TESTMAKER_MYSQL_PWD')}@"
        f"{getenv('TESTMAKER_MYSQL_HOST')}/"
        f"{getenv('TESTMAKER_MYSQL_DB')}")


class DBStorage:
    """persists to mysql server"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine(conn, pool_pre_ping=True)
        if getenv('TESTMAKER_ENV') == 'test':
            Basemetadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current session"""
        new_dict = {}
        if not cls:
            for clss in classes:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        elif cls.__name__ in classes:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def close(self):
        """end a session"""
        self.__session.close()

    def get(self, cls, id):
        from models import storage
        """returns the object based on the class and its ID"""
        obj_key = cls.__name__ + "." + id
        if obj_key in storage.all(cls):
            return storage.all(cls)[obj_key]

    def count(self, cls=None):
        from models import storage
        """return count of objects in storage"""
        if cls:
            return len(storage.all(cls))
        return len(storage.all())
