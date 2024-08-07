#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
import MySQLdb
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO


DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorage(unittest.TestCase):
    """Testing DB Storage"""

    @unittest.skipIf(models.storage_t != 'db', "Tests for db only")
    @classmethod
    def setUpClass(cls) -> None:
        """
        Setting up db connection
        """
        HBNB_MYSQL_USER = 'hbnb_test'
        HBNB_MYSQL_PWD = 'hbnb_test_pwd'
        HBNB_MYSQL_HOST = 'localhost'
        HBNB_MYSQL_DB = 'hbnb_test_db'
        cls.conn = MySQLdb.connect(host=HBNB_MYSQL_HOST, user=HBNB_MYSQL_USER,
                                   passwd=HBNB_MYSQL_PWD, db=HBNB_MYSQL_DB,
                                   port=3306)
        cls.cur = cls.conn.cursor()
        cls.db_instance = DBStorage()
        cls.db_instance.reload()

    def setUp(self) -> None:
        """
        method executed before each test
        """
        self.cmd = HBNBCommand()

    def tearDown(self) -> None:
        """
        method executed after each test
        """
        pass

    @unittest.skipIf(models.storage_t != 'db', "Tests for db only")
    def test_inserting_row(self):
        """
        Tests for create operations
        """
        pass

    @unittest.skipIf(models.storage_t != 'db', "Tests for db only")
    @patch('sys.stdout', new_callable=StringIO)
    def test_get_method(self, mock_stdout):
        """Tests for get method"""
        self.cmd.onecmd('create State name="cairo"')
        state_id = mock_stdout.getvalue().strip()
        state = self.db_instance.get(cls=State, id=state_id)
        self.assertEqual(state_id, state.id)  # Not workinggg

    @unittest.skipIf(models.storage_t != 'db', "Tests for db only")
    @patch('sys.stdout', new_callable=StringIO)
    def test_count_method(self, mock_stdout):
        """Tests for count method"""
        count = 0
        self.cmd.onecmd('create State name="Riyadh"')
        s_1_id = mock_stdout.getvalue().strip()
        count += 1
        self.cmd.onecmd('create State name="Cairo"')
        s_2_id = mock_stdout.getvalue().strip()
        count += 1
        self.cmd.onecmd('create State name="Jeddah"')
        s_3_id = mock_stdout.getvalue().strip()
        count += 1
        self.assertEqual(count, self.db_instance.count(State))
        self.cmd.onecmd(f'create City state_id={s_1_id} name="Olaya"')
        count += 1
        self.cmd.onecmd(f'create City state_id={s_2_id} name="Giza"')
        count += 1
        self.cmd.onecmd(f'create City state_id={s_3_id} name="El-Jazerah"')
        count += 1
        self.assertEqual(count, self.db_instance.count())

    @unittest.skipIf(models.storage_t != 'db', "Tests for db only")
    def test_updating_column(self):
        """
        Tests for Update Operation
        """
        pass

    @unittest.skipIf(models.storage_t != 'db', "Tests for db only")
    def test_deleting_row(self):
        """
        Tests for Delete operation
        """
        pass

    @unittest.skipIf(models.storage_t != 'db', "Tests for db only")
    def test_reading_entity(self):
        """
        Test for create operation
        """
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Closing db connections
        """
        cls.cur.close()
        cls.conn.close()
