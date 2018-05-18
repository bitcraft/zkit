from os.path import splitext


class Asset:

    def __init__(self):
        self.asset_id = None
        self.last_modified = None
        self.notes = None
        self.original_filename = None
        self.properties = dict()
        self.data = None

    def __eq__(self, other):
        return self.get_raw_properties() == other.get_raw_properties()

    @property
    def ext(self):
        _, ext = splitext(self.original_filename)
        return ext

    def get_raw_properties(self):
        return {
            "asset_id": self.asset_id,
            "last_modified": self.last_modified,
            "notes": self.notes,
            "original_filename": self.original_filename,
            "properties": self.properties
        }


class AssetStore:

    def __init__(self, db):
        self.db = db

    def add_asset(self, asset):
        assets = self.db.data.get("assets", dict())
        assets[asset.asset_id] = asset.get_raw_properties()
        self.db.data["assets"] = assets
        self.db.save()

    def delete_asset(self, asset_id):
        del self.db.data["assets"][asset_id]
        self.db.save()

    def update_asset(self, asset):
        self.db.data["assets"][asset.asset_id] = asset.get_raw_properties()
        self.db.save()

    def get_asset(self, asset_id):
        asset_properties = self.db.data["assets"][asset_id]
        asset = Asset()
        asset.asset_id = asset_id
        asset.last_modified = asset_properties["last_modified"]
        asset.notes = asset_properties["notes"]
        asset.original_filename = asset_properties["original_filename"]
        asset.properties = asset_properties["properties"]
        return asset
