from unittest import TestCase

from zkit.assman.relations import RelationStore
from zkit.assman.test_assets import TestDB


class RelationStoreTestCase(TestCase):

    def setUp(self):
        self.db = TestDB()
        self.store = RelationStore(self.db)
        self.store.data = dict()
        self.asset_id = "asdf"
        self.tag_name = "fdsa"
        self.store.add_relation(self.asset_id, self.tag_name)

    def test_can_delete_relation(self):
        self.store.delete_relation(self.asset_id, self.tag_name)
        self.assertEqual(self.db.data["relations"], set())
        self.assertEqual(self.db.calls, ["save", "save"])

    def test_can_delete_relations_by_asset_id(self):
        self.store.delete_relations_by_asset_id(self.asset_id)
        self.assertEqual(self.db.data["relations"], set())
        self.assertEqual(self.db.calls, ["save", "save"])

    def test_can_delete_relations_by_tag_name(self):
        self.store.delete_relations_by_tag_name(self.tag_name)
        self.assertEqual(self.db.data["relations"], set())
        self.assertEqual(self.db.calls, ["save", "save"])

    def test_can_get_relations(self):
        self.assertEqual(self.store.get_relations(), self.db.data["relations"])

    def test_can_get_related_tag_names(self):
        tag_names = self.store.get_related_tag_names(self.asset_id)
        self.assertEqual(tag_names, [self.tag_name])

    def test_can_get_related_asset_ids(self):
        asset_ids = self.store.get_related_asset_ids(self.tag_name)
        self.assertEqual(asset_ids, [self.asset_id])
