from xml.etree import ElementTree as ET
from abc import ABCMeta, abstractmethod

from settings import *

class XmlDataMixin(metaclass=ABCMeta):
    def get_by_ID(self):
        with open(XML_FILE) as f:
            tree = ET.parse(f)
            root = tree.getroot()


class ReprMixin(metaclass=ABCMeta):
    """
    Automatically generates a __repr__-method for any class
    """
    def __repr__(self):
        variables = [f"{k}={v}" if type(v) != str
                     else f'{k}="{v}"'
                     for k,v in vars(self).items()]
        v_string = ", ".join(variables)
        class_name = self.__class__.__name__
        return f"{class_name}({{}})".format(v_string)

class Player(ReprMixin):
    def __init__(self, name, level=1, inventory=None):
        self.name = name
        self.level = level
        if inventory is None:
            self.inventory = Inventory()
        else:
            self.inventory = inventory

class Inventory(ReprMixin):

    ITEMS_LIMIT = 28
    GEAR_SLOTS = {
        "weapon": None,
        "helmet": None,
        "chest":  None,
        "legs":   None,
        "shield": None,
        }

    def __init__(self, gear=None, items=None):
        if gear is None:
            self.gear = []
        else: #TODO: Check for validity
            self.gear = gear

        if items is None:
            self.items = []
        elif len(items) <= self.ITEMS_LIMIT:
            self.items = items
        else:
            raise ValueError(f"Number of items exceeded pre-set limit: {len(items)} > {self.ITEMS_LIMIT}")

        self.itemcount = len(self.items)

    def __len__(self):
        return self.itemcount

    def append(self, item):
        if self.itemcount < self.ITEMS_LIMIT:
            self.items.append(item)
            self.itemcount += 1
        else:
            ValueError("No room in inventory")

class Item(ReprMixin):
    def __init__(self, id_num: int):

        self.name = id_num
        self.slot = id_num
        self.stats = id_num

##gear = [Item(0),
##        Item(1),]
##items = [Item(2),
##         Item(3),
##         Item(4),]
##inv = Inventory(gear=gear, items=items)
##player = Player("Hans", inventory=inv)
##
##for i in gear:
##    print(i)
##print(inv)
##print(player)
