from abc import ABC, abstractmethod


class AssetManager:

    def __init__(self):
        self.asset_db = None
        self.data_store = None
        self.id_provider = None
        self.loaders = dict()

    def get_asset(self, asset_id):
        asset = self.asset_db.get_asset(asset_id)
        self._load_asset(asset)
        return asset

    def _load_asset(self, asset):
        asset_bytes = self.data_store.get_asset_bytes(asset)
        if asset.ext in self.loaders:
            asset.data = self.loaders[asset.ext].load(asset_bytes)
        else:
            asset.data = asset_bytes
        return asset

    def get_assets_with_tag_names(self, *tag_names):
        assets = self.asset_db.get_assets_with_tags(*tag_names)
        for asset in assets:
            self._load_asset(asset)
        return assets

    def store_asset(self, asset, *tag_names):
        if asset.asset_id is None:
            asset.asset_id = self.id_provider.get_next_id()
        self.asset_db.store_asset(asset)
        for tag_name in tag_names:
            self.asset_db.tag_asset(asset.asset_id, tag_name)
        self.data_store.put_asset_bytes(asset.data)


class AssetIDProvider(ABC):

    def __iter__(self):
        while True:
            yield self.get_next_id()

    @abstractmethod
    def get_next_id(self):
        pass


class MediaLoader:

    @abstractmethod
    def load(self, asset):
        pass


class DataStore(ABC):

    @abstractmethod
    def get_asset_bytes(self, asset):
        pass

    @abstractmethod
    def put_asset_bytes(self, asset):
        pass
