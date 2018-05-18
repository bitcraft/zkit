from zkit.assman.assetmanager import DataStore

from os.path import join


class FilesystemDataStore(DataStore):

    def __init__(self, base_directory):
        self.base_directory = base_directory

    def get_asset_bytes(self, asset):
        with open(self._get_asset_path(asset), "rb") as fob:
            return fob.read()

    def put_asset_bytes(self, asset):
        with open(self._get_asset_path(asset), "wb") as fob:
            fob.write(asset.data)

    def _get_asset_path(self, asset):
        filename = str(asset.asset_id).lower() + asset.ext
        return join(self.base_directory, filename)
