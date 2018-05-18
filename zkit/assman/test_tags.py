from unittest import TestCase

from zkit.assman.tags import TagStore
from zkit.assman.tags import Tag
from zkit.assman.test_assets import TestDB


class TagStoreTestCase(TestCase):

    def setUp(self):
        self.db = TestDB()
        self.store = TagStore(self.db)
        self.store.data = dict()
        self.test_tag_name = "asdf"
        self.tag = Tag()
        self.tag.tag_name = self.test_tag_name
        self.store.add_tag(self.tag)

    def test_can_delete_tag(self):
        self.store.delete_tag(self.test_tag_name)
        self.assertEqual(self.db.data["tags"], {})
        self.assertEqual(self.db.calls, ["save", "save"])

    def test_can_update_tag(self):
        self.tag.description = "some notes"
        self.store.update_tag(self.tag)
        self.assertEqual(self.db.calls, ["save", "save"])
        tag_data = self.db.data["tags"][self.test_tag_name]
        self.assertEqual(tag_data, self.tag.get_raw_properties())

    def test_can_get_tag(self):
        tag = self.store.get_tag(self.test_tag_name)
        self.assertEqual(tag.get_raw_properties(),
                         self.tag.get_raw_properties())

    def test_can_check_if_tag_exists(self):
        self.assertTrue(self.store.tag_exists(self.test_tag_name))
        self.assertFalse(self.store.tag_exists("dontexist"))
