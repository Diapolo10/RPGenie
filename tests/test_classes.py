#! python3

""" Pytest-compatible tests for src/classes.py """

import sys

from pathlib import Path
from copy import deepcopy
from unittest import mock

# A workaround for tests not automatically setting
# root/src/ as the current working directory
path_to_src = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(path_to_src))

from classes import Item, Inventory, Player, Character
from settings import *


def initialiser(testcase):
    """ Initialises all test cases with data """
    def inner(*args, **kwargs):
        items = [Item(i) for i in range(kwargs.get("itemcount", 3))]
        inv = Inventory(items=deepcopy(items), **kwargs)
        return testcase(items, inv, *args, **kwargs)
    return inner

@initialiser
def test_testData(items, inv, *args, **kwargs):
    """ Assert the test data itself is valid """
    assert items == inv.items

@initialiser
def test_inv_append(items, inv, *args, **kwargs):
    """ Test for inventory append functionality """
    itemcount = len(items)
    for i in range(inv.max_capacity - itemcount):
        assert inv.append(Item(2)) == f"{Item(2).name} added to inventory"
    assert inv.append(Item(1)) == "No room in inventory"
    assert len(inv) == inv.max_capacity

    #Separate tests for stackable items
    assert inv.append(Item(0)) == f"2 {Item(0).name} in container"
    assert inv.items[inv.items.index(Item(0))]._count == 2

@initialiser
def test_inv_remove(items, inv, *args, **kwargs):
    """ Test for inventory item removal """
    inv.items[inv.items.index(Item(0))]._count += 2

    # Non-stackable items
    assert inv.remove(Item(1)) == f"{Item(1).name} was successfully removed"
    assert inv.items.count(Item(1)) == 0

    # Stackable items
    assert inv.remove(Item(0)) == f"1/{inv.items[inv.items.index(Item(0))]._count+1} {Item(0).name} removed"
    assert inv.items.count(Item(0)) == 1
    assert inv.remove(Item(0), count=3) == "You don't have that many"
    assert inv.remove(Item(0), count=2) == f"{Item(0).name} was successfully removed"
    assert inv.items.count(Item(0)) == 0

@initialiser
def test_inv_equip_unequip(items, inv, *args, **kwargs):
    """ Test for inventory item equip/unequip functionality """

    # Equipping items
    assert inv.equip(Item(1)) == f"You equip {Item(1).name}"
    assert inv.equip(Item(2)) == "You can't equip that"

    # Unequipping items
    assert inv.unequip('weapon') == f"You unequip {Item(1).name}"
    assert inv.unequip('off-hand') == "That slot is empty"
    assert inv.gear['head'] is None
    assert inv.gear['weapon'] is None

@initialiser
def test_inv_combine(items, inv, *args, **kwargs):
    """ Test for item combining functionality """
    assert inv.better_combine_item(inv.items[1], 0, inv.items[2]) == "Combination successful"
    assert len(inv) == 2
    assert inv.better_combine_item(inv.items[0], 0, inv.items[1]) == "Could not combine those items"
    assert len(inv) == 2

def test_char_levelmixin():
    """ Test for level-up functionality """
    char = Character('John Doe', max_level = 5)

    assert 1 == char.level
    assert 85 == char.next_level
    assert char.give_exp(85) == f"Congratulations! You've levelled up; your new level is {char.level}\nEXP required for next level: {int(char.next_level-char.experience)}\nCurrent EXP: {char.experience}"
    for _ in range(char.max_level - char.level):
        char.give_exp(char.next_level)
    assert char.level == char.max_level
    assert char.give_exp(char.next_level) == f""
