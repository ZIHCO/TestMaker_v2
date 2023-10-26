#!/usr/bin/python3
"""instantiate a storage system"""
from os import getenv

if getenv('TESTMAKER_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()
