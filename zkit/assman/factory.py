from os.path import abspath
from os.path import dirname


from zkit.assman.assetmanager import AssetManager
from zkit.assman.filesystemstore import FilesystemAssetStore
from zkit.assman.filesystemstore import FilesystemTagStore
from zkit.assman.pygameloaders import ImageLoader
from zkit.assman.uuidprovider import UUIDProvider


class AssetManagerFactory:

    @staticmethod
    def create_filesystem_manager(asset_module):
        """Creates an asset manager that makes 4 assumptions.
(1) You want to store assets in a module
(2) You want to use UUIDs as asset IDs
(3) You're going to use pygame loaders for images, sounds and fonts
(4) You're going to use exclusively PNG files for images
        """
        manager = AssetManager()
        manager.id_provider = UUIDProvider()
        directory_path = abspath(dirname(asset_module.__file__))
        manager.asset_store = FilesystemAssetStore(directory_path)
        manager.tag_store = FilesystemTagStore(directory_path)
        manager.loaders[".png"] = ImageLoader()
        return manager
