# Built-in libraries
from copy import deepcopy
from abc import ABCMeta, abstractmethod
from typing import List, Dict, Any, NewType

# 3rd-party libraries
# None

# Local libraries
from settings import *
from mixins import *


class Item(ReprMixin, DataFileMixin):

    """ Class for generating item objects; used by Inventory and Player """

    EQUIPMENT = ('weapon',
                 'head',
                 'chest',
                 'legs',
                 'off-hand',)

    def __init__(self, id_num: int, **kwargs) -> None:

        """
        Initiates an Item object

        Arguments:
        - id_num: a unique integer representing the item to be created. Required.

        Optional keyword arguments:
        - file: name of, or path to, a file from which the item data is gathered.
                Defaults to the ITEM_FILE constant.
        - count: for a stackable item, sets how many items are on the stack
        - meta: metadata describing the item, defaults to None
        """

        # Get item data with DataFileMixin.get_item_by_ID()
        item_data = self.get_item_by_ID(
            id_num,
            file=kwargs.get('file', ITEM_FILE)
        )

        # Basic attributes every item has defined
        self.ID = int(id_num)
        self.name = item_data['name']
        self.slot = item_data['type']
        self.descriptions = item_data['examine']
        #NOTE: The item's actual description
        #is defined in the Item.description property!
        #This is due to the distinction between
        #normal and stackable items.

        # Attributes exclusive to wearable items
        if self.slot in self.EQUIPMENT:
            self.attack = item_data.get('atk', None)
            self.defence = item_data.get('def', None)
            self.specialAttack = item_data.get('specialAttack', None)

        # Miscellaneous optional attributes
        self.stackable = item_data.get('stackable', False)
        self.combinations = item_data.get('combine', None)
        self.combinations2 = item_data.get('combine2', None)
        #if self.combinations is not None:
        #    self.combinations = {int(k):int(v) for k,v in self.combinations.items()}
        self.metadata = kwargs.get('meta', None)
        if self.stackable:
            self._count = kwargs.get('count', 1)

    def __eq__(self, item: object) -> bool:
        """ Compares the ID and metadata values of two items """
        if not isinstance(item, Item):
            return NotImplemented
        return self.ID == item.ID and self.metadata == item.metadata

    def __lt__(self, item: object) -> bool:
        if not isinstance(item, Item):
            return NotImplemented
        return self.ID < item.ID

    def __gt__(self, item: object) -> bool:
        if not isinstance(item, Item):
            return NotImplemented
        return self.ID > item.ID

    @property
    def description(self):
        if not self.stackable:
            return self.descriptions
        examine = self.descriptions[0]
        if self._count >= ITEM_MAX_COUNT:
            examine = self.descriptions[1].format(self._count)
        return examine


class Container(ReprMixin):
    """ Class used to create item storages """
    def __init__(self, items: List=None, max_capacity: int=32, **kwargs) -> None:
        """ Initialises Container with default values """
        self.max_capacity = max_capacity

        self.name = kwargs.get('container_name', 'container')

        if items is None:
            self.items: List = []
        elif len(items) <= self.max_capacity:
            self.items = items
        else:
            raise ValueError(f"Cannot initialise container with over {self.max_capacity} items")

    def __len__(self) -> int:
        return len(self.items)

    def append(self, item: Item) -> str:
        add_new = True
        if item.stackable:
            inv_item = next((i for i in self.items if i == item), None)
            if inv_item is not None:
                add_new = False
                inv_item._count += item._count
                return f"{inv_item._count} {item.name} in container"

        if add_new:
            if len(self) < self.max_capacity:
                self.items.append(item)
                return f"{item.name} added to inventory"

        return "No room in inventory"

    def remove(self, item: Item, count: int=1) -> str:
        try:
            if item.stackable:
                inv_item = self.items[self.items.index(item)]
                if inv_item._count < count:
                    return "You don't have that many"
                elif inv_item._count > count:
                    inv_item._count -= count
                    return f"{count}/{inv_item._count+count} {item.name} removed"
                else:
                    self.items.remove(item)
            else:
                self.items.remove(item)
            return f"{item.name} was successfully removed"
        except ValueError:
            return f"{'You don' if self.name=='inventory' else 'The {} doesn'.format(self.name)}'t have any {item.name}s"


class Inventory(Container):
    """ Class used to create player/NPC inventories; extends Container """

    def __init__(self, gear: Dict=None, items: List=None, **kwargs) -> None:

        # Turned into an argument in order to make Inventory class usable by
        # different kinds of entities; including enemies. Some
        # could have three heads, for all I know!
        self.GEAR_SLOTS = kwargs.get('GEAR_SLOTS', {
            "weapon": None,
            "head": None,
            "chest":  None,
            "legs":   None,
            "off-hand": None,
            })

        super().__init__(items=items, max_capacity=kwargs.get('max_capacity', 28), name='inventory', **kwargs)

        if gear is None:
            self.gear = deepcopy(self.GEAR_SLOTS)
        else:
            if len(self.GEAR_SLOTS) == len(gear):
                for key in self.GEAR_SLOTS.keys():
                    if key not in gear:
                        raise ValueError("Equipment key type mismatch")
                else:
                    self.gear = gear
            else:
                raise ValueError("Equipment key count mismatch")

        #self.max_capacity = kwargs.get('max_capacity', 28)

        #if items is None:
        #    self.items = []
        #elif len(items) <= self.max_capacity:
        #    self.items = items
        #else:
        #    raise ValueError(f"Cannot initialise inventory with over {self.max_capacity} items")

    def equip(self, item: Item) -> str:
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

    def equip_from_index(self, item_index: int) -> str:
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

    def unequip(self, slot: str) -> str:
        """ Unequip an item from specified gear slot """
        if self.gear[slot] is not None:
            self.append(self.gear[slot])
            self.gear[slot] = None
            return f"You unequip {self.items[-1].name}"
        else:
            return "That slot is empty"

    def combine_item(self, *items): # NOTE: Replaced by better_combine_item
                                    # DO NOT REMOVE until better_combine_item
                                    # has been fully tested
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

    def better_combine_item(self, base_item: Item, combination: int, *materials) -> str:
        try:
            required_materials = base_item.combinations2[combination][:-1]
            if all(True for mat in required_materials
                   if mat in map(lambda x: x.ID, materials)):
                self.append(Item(base_item.combinations2[combination][-1]))
                self.remove(base_item)
                for material in materials:
                    self.remove(material)
                return "Combination successful"
            return "Could not combine those items"
        except (IndexError, TypeError):
            return "Could not combine those items"
        except Exception as e:
            return f"An unexpected problem has occurred: {e}"


class Character(ReprMixin, LevelMixin, SpritesMixin, metaclass=ABCMeta):
    """ Base class for creating characters """
    #TODO: add more methods

    def __init__(self, name, inventory: Inventory=None, **kwargs) -> None:
        self.name = name
        inventory_size = kwargs.get('inventory_size', 28)
        if inventory is None:
            self.inventory = Inventory(capacity=inventory_size)
        else:
            self.inventory: Inventory = inventory
        #super(Character, self).__init__(**kwargs)
        LevelMixin.__init__(self, **kwargs)
        self.load_char_sprites(self.name)

class Player(Character):
    """ Base class for player objects """
    def __init__(self, name, inventory: Inventory=None, **kwargs) -> None:
        """
        Initialises a player object

        name: player's (character) name
        inventory: an Inventory object that functions as the player's inventory
        """
        super(Player, self).__init__(name, inventory, **kwargs)

if __name__ == "__main__":
    # Initialise all classes for testing
    item = Item(0)
    cont = Container()
    inv = Inventory()
    char = Character('John Doe')
    player = Player('Jane Doe')
