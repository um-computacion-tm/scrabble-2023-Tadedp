import unittest
from unittest.mock import patch
from game.models import (
    EmptyBagException,
    OccupiedSquareException,
    MissingTileInRackException,
    Tile, 
    TileBag,
    Square,
    Board,
    Player
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
        self.assertEqual(square.tile, None)
    
    def testPremiumSquare(self):
        square = Square(3, 'W')
        self.assertEqual(square.multiplier, 3)
        self.assertEqual(square.bonusType, 'W')
        self.assertEqual(square.tile, None)
        
    def testPutTile(self):
        tile = Tile('', 0)
        square = Square(2, 'W')
        square.putTile(tile)
        self.assertEqual(square.tile, tile)
        
    def testSquareValueLetterBonus(self):
        square = Square(3)
        tile = Tile('Z', 10)
        square.putTile(tile)
        result = square.squareValue()
        self.assertEqual(result, 30)
        
    def testSquareValueWordBonus(self):
        square = Square(2, 'W')
        tile = Tile('Z', 10)
        square.putTile(tile)
        result = square.squareValue()
        self.assertEqual(result, 10)
        
    def testSquareValueNoTile(self):
        square = Square(2)
        result = square.squareValue()
        self.assertEqual(result, 0)
        
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
                self.assertEqual(board.board[i][j].tile, None)
    
    def testBoardPut(self):
        board = Board()
        tile = Tile('A', 1)
        board.put(tile, (3, 5))
        self.assertEqual(board.board[3][5].tile, tile)
        
    def testOccupiedSquare(self):
        board = Board()
        tile = Tile('H', 4)
        board.put(tile, (8, 2))
        tile2 = Tile('O', 1)
        with self.assertRaises(OccupiedSquareException):
            board.put(tile2, (8, 2))
        self.assertEqual(board.board[8][2].tile, tile)
    
    def testBoardHorizontalWordScore(self):
        board = Board()
        tile = Tile('H', 4)
        tile2 = Tile('A', 1)
        tile3 = Tile('S', 1)
        board.put(tile, (5, 5))
        board.put(tile2, (5, 6))
        board.put(tile3, (5, 7))
        self.assertEqual(board.wordScore(3, (5,5), 1), 14)

    def testBoardVerticalWordScore(self):
        board = Board()
        tile = Tile('S', 1)
        tile2 = Tile('T', 1)
        tile3 = Tile('O', 1)
        tile4 = Tile('P', 3)
        board.put(tile, (0, 0))
        board.put(tile2, (1, 0))
        board.put(tile3, (2, 0))
        board.put(tile4, (3, 0))
        self.assertEqual(board.wordScore(4, (0,0), 0), 27)

class TestPlayer(unittest.TestCase):
    def testPlayer(self):
        player = Player()
        self.assertEqual(player.rack, [])
        self.assertEqual(player.score, 0)
    
    def testTakeATile(self):
        player = Player()
        tile = Tile('D', 2)
        player.takeTiles([tile])
        self.assertEqual(player.rack, [tile])
        
    def testTakeTiles(self):
        player = Player()
        tile = Tile('D', 2)
        tile2 = Tile('C', 3)
        tile3 = Tile('B', 3)
        player.takeTiles([tile, tile2, tile3])
        self.assertEqual(player.rack, [tile, tile2, tile3])
    
    def testGiveATile(self):
        player = Player()
        tile1 = Tile('S', 1)
        tile2 = Tile('B', 3)
        tile3 = Tile('O', 1)
        tile4 = Tile('S', 1)
        tile5 = Tile('T', 1)
        tile6 = Tile('M', 3)
        tile7 = Tile('F', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        result = player.giveTiles("f")
        self.assertEqual(result, [tile7]) 
        self.assertEqual(player.rack, [tile1, tile2, tile3, tile4, tile5, tile6])
    
    def testGiveTiles(self):
        player = Player()
        tile1 = Tile('S', 1)
        tile2 = Tile('B', 3)
        tile3 = Tile('O', 1)
        tile4 = Tile('S', 1)
        tile5 = Tile('T', 1)
        tile6 = Tile('M', 3)
        tile7 = Tile('F', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        result = player.giveTiles("OsM")
        self.assertEqual(result, [tile3, tile1, tile6]) 
        self.assertEqual(player.rack, [tile2, tile4, tile5, tile7])
    
    def testMissingFirstTile(self):
        player = Player()
        tile1 = Tile('S', 1)
        tile2 = Tile('B', 3)
        tile3 = Tile('O', 1)
        tile4 = Tile('S', 1)
        tile5 = Tile('T', 1)
        tile6 = Tile('M', 3)
        tile7 = Tile('F', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        with self.assertRaises(MissingTileInRackException):
            result = player.giveTiles("R") 
        self.assertEqual(player.rack, [tile1, tile2, tile3, tile4, tile5, tile6, tile7])
    
    def testMissingTile(self):
        player = Player()
        tile1 = Tile('S', 1)
        tile2 = Tile('B', 3)
        tile3 = Tile('O', 1)
        tile4 = Tile('S', 1)
        tile5 = Tile('T', 1)
        tile6 = Tile('M', 3)
        tile7 = Tile('F', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        with self.assertRaises(MissingTileInRackException):
            result = player.giveTiles("MpOf") 
        self.assertEqual(player.rack, [tile1, tile2, tile3, tile4, tile5, tile6, tile7])

if __name__ == '__main__':
    unittest.main()