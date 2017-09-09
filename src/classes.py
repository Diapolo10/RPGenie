# Built-in libraries
from copy import deepcopy
from abc import ABCMeta, abstractmethod

# 3rd-party libraries
# None

# Local libraries
from settings import *
from mixins import *


class Item(ReprMixin, TomlDataMixin):

    """ Class for generating item objects; used by Inventory and Player """

    EQUIPMENT = ('weapon',
                 'head',
                 'chest',
                 'legs',
                 'off-hand',)

    def __init__(self, id_num: int, **kwargs):

        """
        Initiates an Item object

        Arguments:
        - id_num: an unique integer representing the item to be created. Required.

        Optional keyword arguments:
        - file: name of, or path to, a file from which the item data is gathered.
                Defaults to the ITEM_FILE constant.
        - meta: metadata describing the item, defaults to None
        """

        # Get item data with TomlDataMixin.get_item_by_ID()
        item_data = self.get_item_by_ID(
            id_num,
            file=kwargs.get('file', ITEM_FILE)
        )

        # Basic attributes every item has defined
        self.ID = str(id_num)
        self.name = item_data['name']
        self.slot = item_data['type']

        # Attributes exclusive to wearable items
        if self.slot in self.EQUIPMENT:
            self.attack = item_data.get('atk', None)
            self.defence = item_data.get('def', None)
            self.specialAttack = item_data.get('specialAttack', None)

        # Miscellaneous optional attributes
        self.stackable = item_data.get('stackable', False)
        self.combinations = item_data.get('combine', None)
        self.metadata = kwargs.get('meta', None)

    def __eq__(self, item):
        """ Compares the ID and metadata values of two items """
        return self.ID == item.ID and self.metadata == item.metadata

    def __lt__(self, item):
        try:
            return int(self.ID) < int(item.ID)
        except ValueError:
            if self.ID.isdigit() and not item.ID.isdigit():
                return True
            elif self.ID.isdigit():
                return self.ID < item.ID
            return False

    def __gt__(self, item):
        try:
            return int(self.ID) > int(item.ID)
        except ValueError:
            if self.ID.isdigit() and not item.ID.isdigit():
                return False
            elif self.ID.isdigit():
                return self.ID > item.ID
            return True


class Inventory(ReprMixin):

    """ Class used to create inventories """

    GEAR_SLOTS = {
        "weapon": None,
        "head": None,
        "chest":  None,
        "legs":   None,
        "off-hand": None,
        }

    def __init__(self, gear=None, items=None, **kwargs):
        if gear is None:
            self.gear = deepcopy(self.GEAR_SLOTS)
        else: #TODO: Check for validity
            self.gear = gear

        self.MAX_ITEM_COUNT = kwargs.get('max_item_count', 28)

        if items is None:
            self.items = []
        elif len(items) <= self.MAX_ITEM_COUNT:
            self.items = items
        else:
            raise ValueError(f"Number of items exceeded pre-set limit: {len(items)} > {self.MAX_ITEM_COUNT}")


    def __len__(self):
        return len(self.items)

    def append(self, item: Item):
        if len(self) < self.MAX_ITEM_COUNT:
            self.items.append(item)
        else:
            return "No room in inventory"

    def remove(self, item: Item):
        try:
            self.items.remove(item)
        except ValueError:
            return f"You don't have any {item.name}s"

    def equip(self, item: Item):
        """ Equip an item from inventory """
        try:

            # Ensure the inventory has an instance of the requested item
            self.items.index(item)

            temp = self.gear[item.slot]
            self.gear[item.slot] = item
            self.remove(item)
            if temp is not None:
                self.append(temp)
                return f"You swapped {temp.name} to {item.name}"
            else:
                return f"You equip {item.name}"
        except KeyError:
            return "You can't equip that"
        except ValueError:
            return "You don't have that item in your inventory"

    def equip_from_index(self, item_index: int):
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

    def combine_item(self, *items): #TODO: Improve
        try:
            required_items = items[0].combinations
            self.append(Item(required_items[items[1].ID]))
            for item in items:
                self.remove(item)
            return "Combination successful"
        except (IndexError, KeyError):
            return "Could not combine those items"
        except Exception as e:
            return f"An unexpected problem has occurred: {e}"

class Player(ReprMixin, LevelMixin):
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
