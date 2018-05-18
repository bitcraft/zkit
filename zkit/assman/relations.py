

class RelationStore:

    def __init__(self, db):
        self.db = db

    def add_relation(self, asset_id, tag_name):
        relations = self.db.data.get("relations", set())
        relations.add((asset_id, tag_name))
        self.db.data["relations"] = relations
        self.db.save()

    def delete_relation(self, asset_id, tag_name):
        self.db.data["relations"].remove((asset_id, tag_name))
        self.db.save()

    def delete_relations_by_asset_id(self, asset_id):
        self.db.data["relations"] = {
            (a, t) for a, t in self.db.data["relations"]
            if a != asset_id
        }
        self.db.save()

    def delete_relations_by_tag_name(self, tag_name):
        self.db.data["relations"] = {
            (a, t) for a, t in self.db.data["relations"]
            if t != tag_name
        }
        self.db.save()

    def get_relations(self):
        return self.db.data["relations"]

    def get_related_tag_names(self, asset_id):
        return [t for a, t in self.db.data["relations"] if a == asset_id]

    def get_related_asset_ids(self, tag_name):
        return [a for a, t in self.db.data["relations"] if t == tag_name]
