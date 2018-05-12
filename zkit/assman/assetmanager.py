from abc import ABC, abstractmethod

from os.path import splitext

from zkit.assman.tagstore import TagStore


class Asset:

    def __init__(self, asset_id):
        self.asset_id = asset_id
        self.original_filename = None
        self.last_modified = None
        self.properties = dict()
        self.data = None
        self.tag_names = set()


class AssetManager:

    def __init__(self):
        self.id_provider = None
        self.loaders = dict()
        self.asset_store = None
        self.tag_store = None
        self._asset_memo = dict()  # {asset_id: asset}
        self._tag_index = dict()  # {tag_name: asset}

    def __getitem__(self, asset_id):
        asset = self.asset_store.get_asset(asset_id)
        _, extension = splitext(asset.original_filename)
        loader = self.loaders[extension]
        loader.load(asset)
        return asset

    def __setitem__(self, asset):
        asset.asset_id = self.id_provider.get_next_id()
        if not all(name in self.tag_store for name in asset.tag_names):
            msg = "Asset '%s' specifies tag name '%s' which does not exist"
            args = (str(asset.asset_id).lower(), msg)
            raise TagStore.NoSuchTagException(msg % args)
        self.asset_store.put_asset(asset)

    def __delitem__(self, asset_id):
        del self._asset_memo[asset_id]

    def __iter__(self):
        """Iterate through unloaded assets. The returned assets will only
contain meta data, but not the actual content of the files"""
        for asset in self._loader.list_assets():
            yield asset

    def create_tag(self, tag_name, description):
        self.tag_store[tag_name] = description


class AssetIDProvider(ABC):

    def __iter__(self):
        while True:
            yield self.get_next_id()

    @abstractmethod
    def get_next_id(self):
        pass


class AssetStore(ABC):

    @abstractmethod
    def put_asset(self, asset):
        pass

    @abstractmethod
    def get_asset(self, asset_id):
        pass

    @abstractmethod
    def list_assets(self):
        pass


class AssetLoader:

    @abstractmethod
    def load(self, asset):
        pass
