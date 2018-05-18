

class AssetDB:

    class NoSuchTagException(Exception):
        pass

    def __init__(self, asset_store, tag_store, relation_store):
        self.asset_store = asset_store
        self.tag_store = tag_store
        self.relation_store = relation_store

    def store_asset(self, asset):
        self.asset_store.add_asset(asset)

    def store_tag(self, tag):
        self.tag_store.add_tag(tag)

    def tag_asset(self, asset_id, tag_name):
        if not self.tag_store.tag_exists(tag_name):
            raise self.NoSuchTagException(tag_name)
        self.relation_store.add_relation(asset_id, tag_name)

    def untag_asset(self, asset_id, tag_name):
        self.relation_store.delete_relation(asset_id, tag_name)

    def delete_tag(self, tag_name):
        for asset_id in self.relation_store.get_related_asset_ids(tag_name):
            self.relation_store.delete_relation(asset_id, tag_name)
        self.tag_store.delete_tag(tag_name)

    def delete_asset(self, asset_id):
        for tag_name in self.relation_store.get_related_tag_names(asset_id):
            self.relation_store.delete_relation(asset_id, tag_name)
        self.asset_store.delete_asset(asset_id)

    def get_asset(self, asset_id):
        return self.asset_store.get_asset(asset_id)

    def get_tag(self, tag_name):
        return self.tag_store.get_tag(tag_name)

    def get_assets_with_tags(self, *tag_names):
        asset_ids = list()
        for t in tag_names:
            asset_ids.extend(self.relation_store.get_related_asset_ids(t))
        return [self.asset_store.get_asset(a) for a in asset_ids]
