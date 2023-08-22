import unittest
from unittest.mock import patch
from game.models import (
    EmptyBagException,
    OccupiedSquareException,
    Tile, 
    TileBag,
    Square,
    Board
    )

class TestTile(unittest.TestCase):
    def testTile(self):
        tile = Tile('A', 1)
        self.assertEqual(tile.letter, 'A')
        self.assertEqual(tile.value, 1)
    
class TestTileBag(unittest.TestCase):
    @patch('random.shuffle')
    def testTileBag(self, patch_shuffle):
        bag = TileBag()
        self.assertEqual(len(bag.tiles), 100)
        self.assertEqual(patch_shuffle.call_count, 1)
        self.assertEqual(patch_shuffle.call_args[0][0], bag.tiles)
    
    def testBagTake(self):
        bag = TileBag()
        tiles = bag.take(2)
        self.assertEqual(len(bag.tiles), 98)
        self.assertEqual(len(tiles), 2)
        
    def testIncompleteBagTake(self):
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
    
    def testBagPut(self):
        bag = TileBag()
        putTiles = [Tile('Z',1), Tile('Y',1)]
        bag.put(putTiles)
        self.assertEqual(len(bag.tiles), 102)
        
class TestSquare(unittest.TestCase):
    def testSimpleSquare(self):
        square = Square()
        self.assertEqual(square.multiplier, 1)
        self.assertEqual(square.bonusType, 'L')
    
    def testPremiumSquare(self):
        square = Square(3, 'W')
        self.assertEqual(square.multiplier, 3)
        self.assertEqual(square.bonusType, 'W')
        
class TestBoard(unittest.TestCase):
    def testBoardSize(self):
        board = Board()
        self.assertEqual(len(board.board), 15)
        for i in range(15):
            self.assertEqual(len(board.board[i]), 15)
    
    def testBoardSquares(self):
        board = Board()
        for i in range(15):
            for j in range(15):
                self.assertEqual(board.board[i][j][1], None)
    
    def testBoardPut(self):
        board = Board()
        tile = Tile('A', 1)
        board.put(tile, (3, 5))
        self.assertEqual(board.board[3][5][1], tile)
        
    def testOccupiedSquare(self):
        board = Board()
        tile = Tile('H', 4)
        board.put(tile, (8, 2))
        tile2 = Tile('O', 1)
        with self.assertRaises(OccupiedSquareException):
            board.put(tile2, (8, 2))
        self.assertEqual(board.board[8][2][1], tile)
        
if __name__ == '__main__':
    unittest.main()