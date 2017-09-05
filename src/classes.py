# Built-in libraries
from copy import deepcopy
from abc import ABCMeta, abstractmethod

# 3rd-party libraries
import toml

# Local libraries
from settings import *
from mixins import *

class Item(ReprMixin, TomlDataMixin):

    """ Class for generating item objects; used by Inventory and Player """

    EQUIPMENT = ('weapon',
                 'helmet',
                 'chest',
                 'legs',
                 'shield',)

    def __init__(self, id_num: int, **kwargs):
        item_data = self.get_item_by_ID(
            id_num,
            file=kwargs.get('file', ITEM_FILE)
        )
        self.name = item_data['name']
        self.slot = item_data['type']
        if self.slot in self.EQUIPMENT:
            self.attack = item_data.get('atk', None)
            self.defence = item_data.get('def', None)
            self.specialAttack = item_data.get('specialAttack', None)

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
            self.gear = deepcopy(self.GEAR_SLOTS)
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

    def append(self, item: Item):
        if self.itemcount < self.ITEMS_LIMIT:
            self.items.append(item)
            self.itemcount += 1
        else:
            return "No room in inventory"

    def remove(self, item: Item):
        try:
            self.items.remove(item)
            self.itemcount -= 1
        except ValueError:
            return f"You don't have any {item.name}s"

    def equip(self, item_index: int):
        """ Equip an item from inventory at the specified index. """
        try:
            item = self.items[item_index] # Find the item to be equipped
            temp = self.gear[item.slot]   # Temporarily store the currently equipped item (if any)
            self.gear[item.slot] = item   # Equip item
            self.remove(item)             # Remove equipped item from inventory
            if temp is not None:
                self.append(temp)
                return f"You swapped {temp.name} to {item.name}"
            else:
                return f"You equip {item.name}"
        except KeyError:
            return "You can't equip that"
        except IndexError:
            return "There's nothing in that inventory space"

    def unequip(self, slot: str):
        if self.gear[slot] is not None:
            self.append(self.gear[slot])
            self.gear[slot] = None
            return f"You unequip {self.items[-1].name}"
        else:
            return "That slot is empty"

class Player(ReprMixin):
    """ Base class for player objects """
    def __init__(self, name, inventory=None):
        """
        Initialises a player object

        name: player's (character) name
        inventory: an Inventory() object that functions as the player's inventory
        """
        self.name = name
        if inventory is None:
            self.inventory = Inventory()
        else:
            self.inventory = inventory

if __name__ == "__main__":
    pass
