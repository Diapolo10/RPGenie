#TODO: Write tests compatible with pytest

import sys, os
from copy import deepcopy
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')

from classes import Item, Inventory, Player
from settings import *

items = [Item(i) for i in range(3)]
inv = Inventory(items=deepcopy(items))

def test_inv():
    assert items == inv.items
    assert inv.append(Item(1)) is None
    assert len(inv) == len(items)+1
    assert inv.equip(0) == f"You equip {items[0].name}"
    assert inv.unequip('weapon') == f"You unequip {items[0].name}"
    assert inv.combine_item(inv.items[0], inv.items[3]) == "Combination successful"
    assert len(inv) == 3
