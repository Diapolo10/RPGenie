import unittest
from classes import Player

class Tests(unittest.TestCase):
    def test_Player(self):
        plname = "John Doe"
        player = Player(name=plname)
        self.assertEqual(f'Player(name="{plname}", level=1, inventory=Inventory(gear=[], items=[], itemcount=0))', repr(player))
    def test_Inventory(self):#TODO: Add test_Inventory when items implemented in XML
        pass

if __name__ == "__main__":
    unittest.main()
