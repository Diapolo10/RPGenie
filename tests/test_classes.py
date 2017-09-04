#TODO: Write tests compatible with pytest

from src.classes import *
from src.mixins import *
from src.settings import *

items = [Item(i) for i in range(3)]

def test_item_1():
    assert items[0].name    == "Wooden sword"
    assert items[0].slot    == "weapon"
    assert items[0].attack  == 5
    assert items[0].defence == 3
