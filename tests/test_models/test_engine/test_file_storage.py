#!/usr/bin/python3
"""This module contains testcases for the module
file_storage"""
import inspect
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.engine import file_storage
import pep8
import unittest


class FileStorageDocs(unittest.TestCase):
    """test for documentation and pycodestyle conformance
    """

    @classmethod
    def setUpClass(self):
        """set up for the doc tests"""
        self.fs_f = inspect.getmembers(FileStorage,
                                       inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """test for pep8 conformance"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """test for pep8 conformance"""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/'
                                    'test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage needs a docstring")

    def test_file_storage_methods_docstring(self):
        """Test for the FileStorage methods docstring"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             f"{func[0]} method needs a docstring")
            self.assertTrue(len(func[1].__doc__) >= 1,
                            f"{func[0]} method needs a docstring")


class TestFileStorage(unittest.TestCase):
    """Test the filestorage class"""
    def test_all_returns_dict(self):
        """Test that all returns the returns FileStorage.__objects"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    def test_new(self):
        """test that new adds an object to FileStorage.__objects"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        obj = BaseModel()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        storage.new(obj)
        test_dict[obj_key] = obj
        self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        obj = BaseModel()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        new_dict[obj_key] = obj
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))
