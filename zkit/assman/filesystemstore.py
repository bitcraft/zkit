from json import dump
from json import load
from os.path import join
from os.path import splitext

from zkit.assman.assetmanager import Asset
from zkit.assman.assetmanager import AssetStore
from zkit.assman.tagstore import Tag
from zkit.assman.tagstore import TagStore

META_DATA_FILE_NAME = "meta.json"


class FilesystemAssetStore(AssetStore):

    def __init__(self, directory_path):
        self._directory_path = directory_path
        self._meta_data = None

    def put_asset(self, asset):
        asset_path = self._get_asset_path(asset)
        with open(asset_path, "wb") as fob:
            fob.write(asset.data)

        self._load_metadata()
        self._meta_data[str(asset.asset_id).lower()] = {
            "original_filename": asset.original_filename,
            "properties": asset.properties
        }
        self._save_metadata()

    def _get_asset_path(self, asset):
        _, extension = splitext(asset.original_filename)
        filename = str(asset.asset_id).lower() + extension
        return join(self._directory_path, filename)

    def _load_metadata(self):
        if self._meta_data is None:
            try:
                path = join(self._directory_path, META_DATA_FILE_NAME)
                with open(path, "r") as fob:
                    self.meta_data = load(fob)
            except FileNotFoundError:
                self._meta_data = dict()
        return self._meta_data

    def _save_metadata(self):
        path = join(self._directory_path, META_DATA_FILE_NAME)
        with open(path, "w") as fob:
            dump(self._meta_data, fob, indent=4, sort_keys=True)

    def get_asset(self, asset_id):
        self._load_metadata()
        meta = self._meta_data[asset_id]
        asset = Asset(asset_id)
        self._assign_metadata(asset, meta)
        with open(self._get_asset_path(asset), "rb") as fob:
            asset.data = fob.read()
        return asset

    def _assign_metadata(self, asset, meta):
        asset.original_filename = meta["original_filename"]
        asset.properties = meta["properties"]

    def list_assets(self):
        self._load_metadata()
        assets = list()
        for asset_id, meta in self._meta_data.items():
            asset = Asset(asset_id)
            self._assign_metadata(asset, meta)
            assets.append(asset)
        return assets


class FilesystemTagStore(TagStore):

    def __init__(self, directory_path):
        self._tag_memo = None
        self._directory_path = directory_path

    def __getitem__(self, tag_name):
        self._load_tags()
        description = self._tag_memo[tag_name]
        return Tag(tag_name, description)

    def __setitem__(self, tag_name, description):
        self._tag_memo[tag_name] = description
        self._save_tags()

    def __contains__(self, tag_name):
        self._load_tags()
        return tag_name in self._tag_memo

    def __iter__(self):
        self._load_tags()
        for tag_name, description in self._tag_memo:
            yield Tag(tag_name, description)

    def _load_tags(self):
        path = join(self._directory_path, META_DATA_FILE_NAME)
        try:
            with open(path, "r") as fob:
                self._tag_memo = load(fob).get("tags", {})
        except FileNotFoundError:
            pass

    def _put_tags(self):
        path = join(self._directory_path, META_DATA_FILE_NAME)
        all_data = dict()
        try:
            with open(path, "r") as fob:
                all_data = load(fob)
        except FileNotFoundError:
            pass
        all_data["tags"] = self._tag_memo
        with open(path, "w") as fob:
            dump(all_data, fob)
