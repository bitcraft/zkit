from abc import ABC
from abc import abstractmethod


class Tag:

    def __init__(self, name=None, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return "Tag('%s', '%s')" & (self.name, self.description)


class TagStore(ABC):

    class NoSuchTagException(Exception):
        pass

    @abstractmethod
    def __getitem__(self, tag_name):
        pass

    @abstractmethod
    def __setitem__(self, tag_name, description):
        pass

    @abstractmethod
    def __contains__(self, tag_name):
        pass

    @abstractmethod
    def __iter__(self):
        pass
