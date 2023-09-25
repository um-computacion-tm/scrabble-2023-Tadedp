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
        
    def testOccupiedSquare(self):
        tile = Tile('A', 1)
        square = Square()
        square.putTile(tile)
        tile2 = Tile('Q', 5)
        with self.assertRaises(OccupiedSquareException):
            square.putTile(tile2)
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
        
    def testSquareResetWordBonus(self):
        square = Square(2, 'W')
        square.resetBonus()
        self.assertEqual(square.bonusType, 'L')
        self.assertEqual(square.multiplier, 1)
        
    def testSquareResetLetterBonus(self):
        square = Square(3)
        square.resetBonus()
        self.assertEqual(square.bonusType, 'L')
        self.assertEqual(square.multiplier, 1)
        
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

    def testPutVerticalWord(self):
        board = Board()
        tile1 = Tile('A', 1)
        tile2 = Tile('N', 1) 
        tile3 = Tile('D', 2)
        word = [tile1, tile2, tile3]
        board.putVerticalWord(word, (3, 5))
        
        self.assertEqual(board.board[3][5].tile, tile1)    
        self.assertEqual(board.board[4][5].tile, tile2)
        self.assertEqual(board.board[5][5].tile, tile3)
        
    def testPutWordWithOneWordCombination(self):
        board = Board()
        tile1 = Tile('H', 4)
        tile2 = Tile('A', 1) 
        tile3 = Tile('V', 4)
        tile4 = Tile('E', 1)
        word = [tile1, tile2, tile3, tile4]
        board.putHorizontalWord(word, (8, 2))
        
        tile5 = Tile('H', 4)
        tile6 = Tile('S', 1)
        word2 = [tile5, tile6]
        board.putVerticalWord(word2, (7, 3), [(8, 3)])
        
        self.assertEqual(board.board[8][2].tile, tile1)
        self.assertEqual(board.board[8][3].tile, tile2)
        self.assertEqual(board.board[8][4].tile, tile3)
        self.assertEqual(board.board[8][5].tile, tile4)
        self.assertEqual(board.board[7][3].tile, tile5)
        self.assertEqual(board.board[9][3].tile, tile6)
        
    def testPutWordWithTwoWordCombination(self):
        board = Board()
        tile1 = Tile('C', 3)
        tile2 = Tile('A', 1) 
        tile3 = Tile('R', 1)
        word = [tile1, tile2, tile3]
        board.putHorizontalWord(word, (4, 10))
        
        tile4 = Tile('F', 4)
        tile5 = Tile('I', 1)
        tile6 = Tile('R', 1)
        tile7 = Tile('E', 1)
        word2 = [tile4, tile5, tile6, tile7]
        board.putHorizontalWord(word2, (7, 9))
 
        tile8 = Tile('A', 1)
        tile9 = Tile('B', 3)
        tile10 = Tile('N', 1)
        word3 = [tile8, tile9, tile10]
        board.putVerticalWord(word3, (4, 10), [(4, 10), (7, 10)])
        
        self.assertEqual(board.board[4][10].tile, tile1)
        self.assertEqual(board.board[4][11].tile, tile2)
        self.assertEqual(board.board[4][12].tile, tile3)
        
        self.assertEqual(board.board[7][9].tile, tile4)
        self.assertEqual(board.board[7][10].tile, tile5)
        self.assertEqual(board.board[7][11].tile, tile6)
        self.assertEqual(board.board[7][12].tile, tile7)
        
        self.assertEqual(board.board[5][10].tile, tile8)
        self.assertEqual(board.board[6][10].tile, tile9)
        self.assertEqual(board.board[8][10].tile, tile10)
        
    def testHorizontalWordScore(self):
        board = Board()
        word = [Tile('H', 4), Tile('A', 1), Tile('S', 1)]
        board.putHorizontalWord(word, (5,5))
        self.assertEqual(board.wordScore(3, 1, (5,5)), 14)

    def testVerticalWordScore(self):
        board = Board()
        word = [Tile('S', 1), Tile('T', 1), Tile('O', 1), Tile('P', 3)]
        board.putVerticalWord(word, (0, 0))
        self.assertEqual(board.wordScore(4, 0, (0,0)), 27)
        
    def testThreeWordScores(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putVerticalWord(word1, (11, 0))
        self.assertEqual(board.wordScore(4, 0, (11,0)), 39)
        word2 = [Tile('O', 1), Tile('S', 1), Tile('T', 1), Tile('E', 1), Tile('L', 1)]
        board.putHorizontalWord(word2, (11, 0), [(11, 0)])
        self.assertEqual(board.wordScore(6, 1, (11,0)), 18)
        word3 = [Tile('M', 3), Tile('B', 3), Tile('E', 1), Tile('R', 1)]
        board.putHorizontalWord(word3, (14, 0), [(14, 0)])
        self.assertEqual(board.wordScore(5, 1, (14,0)), 10)
        
    def testVerticalWordIsInside(self):
        board = Board()
        word = "UNIVERSITY"
        wordIsValid = board.wordIsInside(word, 0, (5, 14))
        self.assertTrue(wordIsValid)
    
    def testHorizontalWordIsInside(self):
        board = Board()
        word = "UNIVERSITY"
        wordIsValid = board.wordIsInside(word, 1, (0, 0))
        self.assertTrue(wordIsValid)
    
    def testVerticalWordIsNotInside(self):
        board = Board()
        word = "UNIVERSITY"
        wordIsValid = board.wordIsInside(word, 0, (6, 2))
        self.assertFalse(wordIsValid)
        
    def testHorizontalWordIsNotInside(self):
        board = Board()
        word = "UNIVERSITY"
        wordIsValid = board.wordIsInside(word, 1, (0, 25))
        self.assertFalse(wordIsValid)    
        
    def testPlaceFirstHorizontalWordFine(self):
        board = Board()
        word = "HOME"
        wordIsValid = board.wordIsValid(word, 1, (7, 7))
        self.assertTrue(wordIsValid)
        
    def testPlaceFirstHorizontalWordWrong(self):
        board = Board()
        word = "HOME"
        wordIsValid = board.wordIsValid(word, 1, (7, 0))
        self.assertFalse(wordIsValid)
        
    def testPlaceFirstVerticalWordFine(self):
        board = Board()
        word = "HEART"
        wordIsValid = board.wordIsValid(word, 0, (3, 7))
        self.assertTrue(wordIsValid)
        
    def testPlaceFirstVerticaltWordWrong(self):
        board = Board()
        word = "HEART"
        wordIsValid = board.wordIsValid(word, 0, (8, 7))
        self.assertFalse(wordIsValid)
        
    def testPlaceNotInitialHorizontalWordFine(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putHorizontalWord(word1, (7, 7))
        word2 = "HOMES"
        wordIsValid = board.wordIsValid(word2, 1, (7, 7))
        self.assertTrue(wordIsValid)
        
    def testPlaceNotInitialHorizontalWordWrong(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putVerticalWord(word1, (4, 7))
        word2 = "ENTER"
        wordIsValid = board.wordIsValid(word2, 1, (7, 5))
        self.assertFalse(wordIsValid)
        
    def testPlaceNotInitialVerticalWordFine(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putHorizontalWord(word1, (7, 4))
        word2 = "ENTER"
        wordIsValid = board.wordIsValid(word2, 0, (4, 7))
        self.assertTrue(wordIsValid)        
    
    def testPlaceNotInitialVerticaltWordWrong(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putHorizontalWord(word1, (7, 6))
        word2 = "ENTER"
        wordIsValid = board.wordIsValid(word2, 0, (0, 0))
        self.assertFalse(wordIsValid)        
                
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
        
    def testSumScore(self):
        player = Player()
        self.assertEqual(player.score, 0)
        player.sumScore(15)
        self.assertEqual(player.score, 15)
        player.sumScore(32)
        self.assertEqual(player.score, 47)
    
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
        
    def testHaveTiles(self):
        player = Player()
        tile1 = Tile('S', 1)
        tile2 = Tile('LL', 8)
        tile3 = Tile('O', 1)
        tile4 = Tile('E', 1)
        tile5 = Tile('E', 1)
        tile6 = Tile('H', 4)
        tile7 = Tile('F', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        self.assertEqual(player.haveTiles("hello"), True)
        
    def testDoesntHaveTiles(self):
        player = Player()
        tile1 = Tile('S', 1)
        tile2 = Tile('O', 1)
        tile3 = Tile('O', 1)
        tile4 = Tile('E', 1)
        tile5 = Tile('E', 1)
        tile6 = Tile('H', 4)
        tile7 = Tile('F', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        self.assertEqual(player.haveTiles("hello"), False)        

if __name__ == '__main__':
    unittest.main()