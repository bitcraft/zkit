from uuid import uuid4

from zkit.assman.assetmanager import AssetIDProvider


class UUIDProvider(AssetIDProvider):

    def __iter__(self):
        while True:
            yield uuid4()

    def get_next_id(self):
        return uuid4()
