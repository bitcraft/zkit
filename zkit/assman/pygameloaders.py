from io import BytesIO

from pygame.image import load

from zkit.assman.assetmanager import AssetLoader


# TODO: Extend this loader to take default convert arguments
class ImageLoader(AssetLoader):

    def load(self, asset):
        fob = BytesIO(asset.data)
        image = load(fob, asset.original_filename)
        asset.data = image
