import unittest
from classes import Player, Inventory, Item

class Tests(unittest.TestCase):
    def test_Player(self):
        plname = "John Doe"
        player = Player(name=plname)
        self.assertEqual(f'Player(name="{plname}", level=1, inventory=Inventory(gear={{}}, items=[], itemcount=0))'.format({'weapon': None, 'helmet': None, 'chest': None, 'legs': None, 'shield': None}), repr(player))
    def test_Inventory(self):#TODO: Add test_Inventory when items implemented in XML
        inv = Inventory()
        item = Item(0)
        inv.append(item)
        print(inv)


if __name__ == "__main__":
    unittest.main()
