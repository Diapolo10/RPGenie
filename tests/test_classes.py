#! python3

""" Pytest-compatible tests for src/classes.py """

import sys
import os
from copy import deepcopy
from unittest import mock

# A workaround for tests not automatically setting
# root/src/ as the current working directory
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')

from classes import Item, Inventory, Player
from settings import *


def initialiser(testcase):
    """ Initialises all test cases with data """
    def inner(*args, **kwargs):
        items = [Item(i) for i in range(kwargs.get("itemcount", 3))]
        inv = Inventory(items=deepcopy(items), **kwargs)
        testcase(items, inv, *args, **kwargs)
    return inner

@initialiser
def test_testData(items, inv, *args, **kwargs):
    """ Assert the test data itself is valid """
    assert items == inv.items

@initialiser
def test_inv_append(items, inv, *args, **kwargs):
    """ Test for inventory append functionality """
    itemcount = len(items)
    for i in range(inv.MAX_ITEM_COUNT - itemcount):
        assert inv.append(Item(2)) is None
    assert inv.append(Item(1)) == "No room in inventory"
    assert len(inv) == inv.MAX_ITEM_COUNT

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
    assert inv.combine_item(inv.items[1], inv.items[2]) == "Combination successful"
    assert len(inv) == 2
