import unittest
from unittest.mock import patch
from game.models import (
    EmptyBagException,
    Tile, 
    TileBag
    )

class TestTiles(unittest.TestCase):
    def testTile(self):
        tile = Tile('A', 1)
        self.assertEqual(tile.letter, 'A')
        self.assertEqual(tile.value, 1)
    
class TestBagTiles(unittest.TestCase):
    @patch('random.shuffle')
    def testTileBag(self, patch_shuffle):
        bag = TileBag()
        self.assertEqual(len(bag.tiles), 100)
        self.assertEqual(patch_shuffle.call_count, 1)
        self.assertEqual(patch_shuffle.call_args[0][0], bag.tiles)
    
    def testTake(self):
        bag = TileBag()
        tiles = bag.take(2)
        self.assertEqual(len(bag.tiles), 98)
        self.assertEqual(len(tiles), 2)
        
    def testIncompleteTake(self):
        bag = TileBag()
        tiles = bag.take(98)
        tiles = []
        self.assertEqual(len(bag.tiles), 2)
        tiles = bag.take(5)
        self.assertEqual(len(tiles), 2)
    
    def testEmptyBag(self):
        bag = TileBag()
        tiles = bag.take(100)
        tiles = []
        with self.assertRaises(EmptyBagException):
            tiles = bag.take(1)
        self.assertEqual(len(tiles), 0)
    
    def testPut(self):
        bag = TileBag()
        putTiles = [Tile('Z',1), Tile('Y',1)]
        bag.put(putTiles)
        self.assertEqual(len(bag.tiles), 102)
    


if __name__ == '__main__':
    unittest.main()