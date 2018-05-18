from unittest import TestCase

from zkit.assman.assets import AssetStore
from zkit.assman.assets import Asset


class TestDB:

    def __init__(self):
        self.data = dict()
        self.calls = list()

    def save(self):
        self.calls.append("save")

    def load(self):
        self.calls.append("load")


class AssetStoreTestCase(TestCase):

    def setUp(self):
        self.db = TestDB()
        self.store = AssetStore(self.db)
        self.store.data = dict()
        self.test_id = "asdf"
        self.asset = Asset()
        test_id = "asdf"
        self.asset.asset_id = test_id
        self.store.add_asset(self.asset)

    def test_can_delete_asset(self):
        self.store.delete_asset(self.test_id)
        self.assertEqual(self.db.data["assets"], {})
        self.assertEqual(self.db.calls, ["save", "save"])

    def test_can_update_asset(self):
        self.asset.notes = "some notes"
        self.asset.properties["foo"] = "bar"
        self.store.update_asset(self.asset)
        self.assertEqual(self.db.calls, ["save", "save"])
        asset_data = self.db.data["assets"][self.test_id]
        self.assertEqual(asset_data, self.asset.get_raw_properties())

    def test_can_get_asset(self):
        asset = self.store.get_asset(self.test_id)
        self.assertEqual(asset.get_raw_properties(),
                         self.asset.get_raw_properties())
