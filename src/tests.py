import unittest
from classes import Player

class Tests(unittest.TestCase):
    def test_Player(self):
        player = Player(name="John Doe")
        print(repr(player))

if __name__ == "__main__":
    unittest.main()
