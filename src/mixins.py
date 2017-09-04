# Built-in libraries
from copy import deepcopy
from abc import ABCMeta, abstractmethod

# 3rd-party libraries
import toml

# Local libraries
from settings import *

class TomlDataMixin(metaclass=ABCMeta):
    """
    Contains methods for getting data from TOML-files
    """
    def _get_by_ID(self, ID: int, obj_type: str, file=DATA_FILE) -> dict:
        """ 'Low-level' access to TOML-data """
        with open(file) as f:
            data = toml.load(f)
        return data[obj_type][str(ID)]

    def get_item_by_ID(self, ID: int, file=DATA_FILE) -> dict:
        """ Returns a dictionary representation of a given item ID """
        return self._get_by_ID(ID, 'items', file)

    def get_enemy_by_ID(self, ID: int, file=DATA_FILE) -> dict:
        """ Returns a dictionary representation of a given enemy ID """
        return self._get_by_ID(ID, 'enemies', file)

    def get_npc_by_ID(self, ID: int, file=DATA_FILE) -> dict:
        """ Returns a dictionary representation of a given NPC ID """
        return self._get_by_ID(ID, 'NPCs', file)

    def get_entity_by_ID(self, ID: int, file=DATA_FILE) -> dict:
        """ Returns a dictionary representation of a given entity ID """
        return self._get_by_ID(ID, 'entities', file)


class ReprMixin(metaclass=ABCMeta):
    """
    Automatically generates a __repr__-method for any class
    """
    def __repr__(self):
        """ Automatically generated __repr__-method """
        variables = [f"{k}={v}" if type(v) != str
                     else f'{k}="{v}"'
                     for k,v in vars(self).items()]
        v_string = ", ".join(variables)
        class_name = self.__class__.__name__
        return f"{class_name}({{}})".format(v_string)

class LevelMixin(metaclass=ABCMeta):
    """ Gives standard level-up mechanics for the child class """
    def __init__(self):
        self.level      = 1
        self.experience = 0

    def nextLevel(self):
        exponent = 1.6
        baseXP = 85
        return math.floor(baseXP * (self.level**exponent))

    def levelup(self):
        while True:
            if self.nextLevel() <= self.experience:
                self.level += 1
            else:
                print("EXP required for next level:", int(self.nextLevel()-self.experience))
                break

    def give_xp(self, amount):
        self.experience += amount
