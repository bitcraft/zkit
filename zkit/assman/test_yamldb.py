from os import remove, close
from tempfile import mkstemp
from unittest import TestCase

from zkit.assman.yamldb import YAMLDB


class YAMLFileTestCase(TestCase):

    def setUp(self):
        fob, self.filename = mkstemp()
        close(fob)
        self.db = YAMLDB(self.filename)

    def tearDown(self):
        remove(self.filename)

    def test_can_save_and_load_data(self):
        data = {"foo": {"bar": [1, 2, 3]}}
        self.db.data = data
        self.db.save()
        self.db.data = None
        self.db.load()
        self.assertEqual(data, self.db.data)
