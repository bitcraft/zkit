from unittest import TestCase
from uuid import uuid4

from zkit.assman.assetdb import AssetDB
from zkit.assman.assets import AssetStore, Asset
from zkit.assman.relations import RelationStore
from zkit.assman.tags import TagStore, Tag
from zkit.assman.test_assets import TestDB


class AssetDBTestCase(TestCase):

    def setUp(self):
        self.db = TestDB()
        self.asset_store = AssetStore(self.db)
        self.relation_store = RelationStore(self.db)
        self.tag_store = TagStore(self.db)
        self.asset_db = AssetDB(self.asset_store,
                                self.tag_store,
                                self.relation_store)
        self.asset = Asset()
        self.asset.asset_id = uuid4()
        self.tag = Tag()
        self.tag.tag_name = "foo"
        self.asset_db.store_asset(self.asset)
        self.asset_db.store_tag(self.tag)
        self.asset_db.tag_asset(self.asset.asset_id, self.tag.tag_name)

    def test_can_store_asset(self):
        asset = self.asset_store.get_asset(self.asset.asset_id)
        self.assertEqual(asset, self.asset)

    def test_can_store_tag(self):
        self.asset_db.store_tag(self.tag)
        tag = self.tag_store.get_tag(self.tag.tag_name)
        self.assertEqual(tag, self.tag)

    def test_can_tag_assets(self):
        assets = self.asset_db.get_assets_with_tags(self.tag.tag_name)
        self.assertEqual(assets[0], self.asset)

    def test_cant_tag_asset_with_non_existant_tag(self):
        with self.assertRaises(AssetDB.NoSuchTagException):
            self.asset_db.tag_asset(self.asset.asset_id, "dontexist")

    def test_can_untag_asset(self):
        self.asset_db.untag_asset(self.asset.asset_id, self.tag.tag_name)
        assets = self.asset_db.get_assets_with_tags(self.tag.tag_name)
        self.assertEqual(len(assets), 0)

    def test_can_delete_tag(self):
        self.asset_db.delete_tag(self.tag.tag_name)
        self.assertEqual(len(self.db.data["tags"]), 0)
        assets = self.asset_db.get_assets_with_tags(self.tag.tag_name)
        self.assertEqual(len(assets), 0)

    def test_can_delete_asset(self):
        self.asset_db.delete_asset(self.asset.asset_id)
        self.assertEqual(len(self.db.data["assets"]), 0)

    def test_can_get_asset(self):
        asset = self.asset_db.get_asset(self.asset.asset_id)
        self.assertEqual(asset, self.asset)

    def test_can_get_tag(self):
        self.assertEqual(self.asset_db.get_tag(self.tag.tag_name), self.tag)

    def test_can_get_assets_with_tags(self):
        assets = self.asset_db.get_assets_with_tags(self.tag.tag_name)
        self.assertEqual(assets, [self.asset])
