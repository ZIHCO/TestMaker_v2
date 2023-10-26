#!/usr/bin/python3
"""Testcases for basemodel module"""
from datetime import datetime
import inspect
from models import base_model
from models.base_model import BaseModel
import pep8 as pycodestyle
import time
import unittest
from unittest import mock
module_doc = base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests for documentation and style of BaseModel"""

    @classmethod
    def setUpClass(self):
        """set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """test that module conform to pep8"""
        for path in ['models/base_model.py',
                     'tests/test_models/test_base_model.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """test for module documentation"""
        self.assertIsNot(module_doc, None,
                         "base_module.py needs a docstring")
        self.assertTrue(len(module_doc) > 1,
                        "base_module.py needs a docstring")

    def test_class_docstring(self):
        """test for BaseModel documentation"""
        self.assertIsNot(BaseModel.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(BaseModel.__doc__) > 1,
                        "BaseModel class needs a docstring")

    def test_func_docstring(self):
        """test for BaseModel methods documentation"""
        for func in self.base_funcs:
            print(func)
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBaseModel(unittest.TestCase):
    """test the BaseModel class"""
    def test_instantiation(self):
        """test object creation"""
        obj = BaseModel()
        self.assertIs(type(obj), BaseModel)
        obj.name = "Zihco"
        obj.number = 21
        attrs_types = {
                "id": str,
                "created_at": datetime,
                "updated_at": datetime,
                "name": str,
                "number": int
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, obj.__dict__)
                self.assertIs(type(obj.__dict__[attr]), typ)
        self.assertEqual(obj.name, "Zihco")
        self.assertEqual(obj.number, 21)

    def test_datetime_attributes(self):
        """two objects of BaseModel have different datetime objects
        and that at creation updated_at and created_at are identical"""
        tic = datetime.utcnow()
        inst1 = BaseModel()
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.utcnow()
        inst2 = BaseModel()
        toc = datetime.utcnow()
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test id validity"""
        obj1 = BaseModel()
        obj2 = BaseModel()
        for obj in [obj1, obj2]:
            uuid = obj.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(uuid,
                                 '^[0-9a-f]{8}-[0-9a-f]{4}'
                                 '-[0-9a-f]{4}-[0-9a-f]{4}'
                                 '-[0-9a-f]{12}$')
        self.assertNotEqual(obj1.id, obj2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = ["id",
                          "created_at",
                          "updated_at",
                          "name",
                          "my_number",
                          "__class__"]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d['__class__'], 'BaseModel')
        self.assertEqual(d['name'], "Holberton")
        self.assertEqual(d['my_number'], 89)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    def test_save(self):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)

    def test_recreate(self):
        """recreate an instance from dict representation"""
        obj = BaseModel()
        obj.name = "Zihco"
        obj.age = 27
        dictionary = obj.to_dict()
        new_obj = BaseModel(**dictionary)
        self.assertEqual(type(new_obj.created_at), datetime)
        self.assertIsNot(new_obj, obj)
