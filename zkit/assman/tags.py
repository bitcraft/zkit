

class Tag:

    def __init__(self):
        self.tag_name = None
        self.description = None

    def __eq__(self, other):
        return self.get_raw_properties() == other.get_raw_properties()

    def get_raw_properties(self):
        return {
            "tag_name": self.tag_name,
            "description": self.description
        }


class TagStore:

    def __init__(self, db):
        self.db = db

    def add_tag(self, tag):
        tags = self.db.data.get("tags", dict())
        tags[tag.tag_name] = tag.get_raw_properties()
        self.db.data["tags"] = tags
        self.db.save()

    def delete_tag(self, tag_name):
        del self.db.data["tags"][tag_name]
        self.db.save()

    def update_tag(self, tag):
        self.db.data["tags"][tag.tag_name] = tag.get_raw_properties()
        self.db.save()

    def get_tag(self, tag_name):
        tag_properties = self.db.data["tags"][tag_name]
        tag = Tag()
        tag.tag_name = tag_name
        tag.description = tag_properties["description"]
        return tag

    def tag_exists(self, tag_name):
        return tag_name in self.db.data["tags"]
