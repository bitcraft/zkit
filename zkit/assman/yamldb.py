import yaml

YAML_KWARGS = {
    "explicit_start": True,
    "explicit_end": True,
    "indent": 4,
    "default_flow_style": False,
    "encoding": "utf-8"
}


class YAMLDB:

    def __init__(self, filepath):
        self.filepath = filepath
        self.data = dict()

    def load(self):
        with open(self.filepath, "r") as fob:
            self.data = yaml.load(fob)

    def save(self):
        with open(self.filepath, "w") as fob:
            yaml.dump(self.data, fob, **YAML_KWARGS)
