import unittest
from unittest.mock import patch
from game.models import (
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
    
    def testTileStringRepresentation(self):
        tile = Tile('H', 4)
        self.assertEqual(tile.__repr__(), "[H](4p.)")
        
    
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
    
    def testWordMultiplierSquareStringRepresentation(self):
        square = Square(2, 'W')
        self.assertEqual(square.__repr__(),"Wx2")
    
    def testLetterMultiplierSquareStringRepresentation(self):
        square = Square(3)
        self.assertEqual(square.__repr__(),"Lx3")
    
    def testSquareWithOneLetterStringRepresentation(self):
        square = Square(2, 'W')
        square.tile = Tile(" ", 0)
        self.assertEqual(square.__repr__(),"[ *]")
    
    def testSquareWithTwoLettersStringRepresentation(self):
        square = Square(2, 'W')
        square.tile = Tile("CH", 5)
        self.assertEqual(square.__repr__(),"[CH]")
                         
    
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
        board.putWord(word, 0, (3, 5))
        
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
        board.putWord(word, 1, (8, 2))
        
        tile5 = Tile('H', 4)
        tile6 = Tile('S', 1)
        word2 = [tile5, tile6]
        board.putWord(word2, 0, (7, 3))
        
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
        board.putWord(word, 1, (4, 10))
        
        tile4 = Tile('F', 4)
        tile5 = Tile('I', 1)
        tile6 = Tile('R', 1)
        tile7 = Tile('E', 1)
        word2 = [tile4, tile5, tile6, tile7]
        board.putWord(word2, 1, (7, 9))
 
        tile8 = Tile('A', 1)
        tile9 = Tile('B', 3)
        tile10 = Tile('N', 1)
        word3 = [tile8, tile9, tile10]
        board.putWord(word3, 0, (4, 10))
        
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
       board.putWord(word, 1, (5,5))
       self.assertEqual(board.wordScore(3, 1, (5,5)), 14)

    def testVerticalWordScore(self):
        board = Board()
        word = [Tile('S', 1), Tile('T', 1), Tile('O', 1), Tile('P', 3)]
        board.putWord(word, 0, (0, 0))
        self.assertEqual(board.wordScore(4, 0, (0,0)), 27)
            
    def testThreeWordScores(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 0, (11, 0))
        self.assertEqual(board.wordScore(4, 0, (11,0)), 39)
        word2 = [Tile('O', 1), Tile('S', 1), Tile('T', 1), Tile('E', 1), Tile('L', 1)]
        board.putWord(word2, 1, (11, 0))
        self.assertEqual(board.wordScore(6, 1, (11,0)), 18)
        word3 = [Tile('M', 3), Tile('B', 3), Tile('E', 1), Tile('R', 1)]
        board.putWord(word3, 1, (14, 0))
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
        
    def testPlaceFirstWordTooShort(self):
        board = Board()
        word = "Y"
        wordIsValid = board.wordIsValid(word, 1, (7, 7))
        self.assertFalse(wordIsValid)    
        
    def testPlaceFirstHorizontalWordFine(self):
        board = Board()
        word = "HOME"
        wordIsValid = board.wordIsValid(word, 1, (7, 7))
        self.assertTrue(wordIsValid)
        
    def testPlaceFirstHorizontalWordWrong(self):
        board = Board()
        word = "HOME"
        wordIsValid = board.wordIsValid(word, 1, (6, 7))
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

    def testPlaceNotInitialAdjacentHorizontalWordFine(self):
        board = Board()
        word1 = [Tile('R', 1), Tile('A', 1), Tile('S', 1), Tile('H', 4)]
        board.putWord(word1, 1, (7, 7))
        word2 = "TEA"
        wordIsValid = board.wordIsValid(word2, 0, (7, 6))
        self.assertTrue(wordIsValid)
            
    def testPlaceNotInitialAdjacentHorizontalWordWrong(self):
        board = Board()
        word1 = [Tile('T', 1), Tile('O', 1), Tile('Y', 3)]
        board.putWord(word1, 1, (7, 7))
        word2 = [Tile('H', 4), Tile('O', 1), Tile('P', 3)]
        board.putWord(word2, 1, (7, 11))
        word3 = "SHOP"
        wordIsValid = board.wordIsValid(word3, 1, (7, 10))
        self.assertFalse(wordIsValid)
            
    def testPlaceNotInitialAdjacentVerticalWordFine(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 0, (7, 7))
        word2 = "BY"
        wordIsValid = board.wordIsValid(word2, 0, (8, 8))
        self.assertTrue(wordIsValid)
            
    def testPlaceNotInitialAdjacentVerticalWordWrong(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('A', 1), Tile('S', 1)]
        board.putWord(word1, 0, (7, 7))
        word2 = "OK"
        wordIsValid = board.wordIsValid(word2, 0, (9, 5))
        self.assertFalse(wordIsValid)    
        
    def testPlaceNotInitialHorizontalWordFine(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 1, (7, 7))
        word2 = "HOMES"
        wordIsValid = board.wordIsValid(word2, 1, (7, 7))
        self.assertTrue(wordIsValid)
            
    def testPlaceNotInitialHorizontalWordWrong(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 0, (4, 7))
        word2 = "ENTER"
        wordIsValid = board.wordIsValid(word2, 1, (7, 5))
        self.assertFalse(wordIsValid)
            
    def testPlaceNotInitialVerticalWordFine(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 1, (7, 4))
        word2 = "CHERRIES"
        wordIsValid = board.wordIsValid(word2, 0, (6, 7))
        self.assertTrue(wordIsValid)        
        
    def testPlaceNotInitialVerticaltWordWrong(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 1, (7, 6))
        word2 = "ENTER"
        wordIsValid = board.wordIsValid(word2, 0, (0, 0))
        self.assertFalse(wordIsValid)  
        
    def testOneFormedWord(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 1, (7, 7))
        word2 = "HOMES"
        words = board.formedWords(word2, 1, (7, 7))
        cell1 = board.board[7][7]
        cell2 = board.board[7][8]
        cell3 = board.board[7][9]
        cell4 = board.board[7][10]
        cell5 = board.board[7][11]
        self.assertEqual(words, [["HOMES", cell1, cell2, cell3, cell4, cell5]])
        
    def testTwoFormedWords(self):
        board = Board()
        word1 = [Tile('G', 4), Tile('O', 1)]
        board.putWord(word1, 1, (7, 7))
        word2 = "EMERALD"
        words = board.formedWords(word2, 0, (7, 6))
        cell1 = board.board[7][6]
        cell2 = board.board[8][6]
        cell3 = board.board[9][6]
        cell4 = board.board[10][6]
        cell5 = board.board[11][6]
        cell6 = board.board[12][6]
        cell7 = board.board[13][6]
        cell8 = board.board[7][7]
        cell9 = board.board[7][8]
        self.assertEqual(words, [["EMERALD", cell1, cell2, cell3, cell4, cell5, cell6, cell7]
                                 ,["EGO", cell1, cell8, cell9]])
            
    def testThreeFormedWords(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 0, (7, 7))
        word2 = [Tile('G', 2), Tile('E', 1), Tile('M', 3)]
        board.putWord(word2, 0, (7, 9))
        word3 = "DO"
        words = board.formedWords(word3, 0, (8, 8))
        cell1 = board.board[8][8]
        cell2 = board.board[9][8]
        cell3 = board.board[8][7]
        cell4 = board.board[8][9]
        cell5 = board.board[9][7]
        cell6 = board.board[9][9]
        self.assertEqual(words, [["DO", cell1, cell2], ["ODE", cell3, cell1, cell4], 
                                 ["MOM", cell5, cell2, cell6]])

    def testThreeFormedWordsComplex(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('O', 1), Tile('M', 3), Tile('E', 1)]
        board.putWord(word1, 0, (7, 7))
        word2 = "BY"
        words = board.formedWords(word2, 0, (8, 8))
        cell1 = board.board[8][8]
        cell2 = board.board[9][8]
        cell3 = board.board[8][7]
        cell4 = board.board[9][7]
        self.assertEqual(words, [["BY", cell1, cell2], ["OB", cell3, cell1], ["MY", cell4, cell2]])

    def testFourFormedWords(self):
        board = Board()
        word1 = [Tile('H', 4), Tile('A', 1)]
        board.putWord(word1, 1, (7, 7))
        word2 = [Tile('F', 4), Tile('O', 1), Tile('R', 1)]
        board.putWord(word2, 1, (9, 9))
        word3 = "ABO"
        words = board.formedWords(word3, 1, (8, 7))
        cell1 = board.board[8][7]
        cell2 = board.board[8][8]
        cell3 = board.board[8][9]
        cell4 = board.board[7][7]
        cell5 = board.board[7][8]
        cell6 = board.board[9][9]
        self.assertEqual(words, [["ABO", cell1, cell2, cell3], ["HA", cell4, cell1], 
                                 ["AB", cell5, cell2], ["OF", cell3, cell6]])

    def testRemoveWordBoardTiles(self):
        board = Board()
        word1 = [Tile('O', 1), Tile('N', 1)]
        board.putWord(word1, 1, (7, 7))
        word2 = "NONE"
        cutWord = board.removeWordBoardTiles(word2, 1, (7,6))
        self.assertEqual(cutWord, "NE")
                
    def testRemoveWordBoardTilesComplex(self):
        board = Board()
        word1 = [Tile('CH', 5), Tile('O', 1), Tile('O', 1), Tile('S', 1), Tile('E', 1)]
        board.putWord(word1, 0, (7, 7))
        word2 = "CHERRIES"
        cutWord = board.removeWordBoardTiles(word2, 1, (7,7))
        self.assertEqual(cutWord, "ERRIES")

    def testBoardStringRepresentation(self):
        board = Board()
        self.assertEqual(board.__repr__(), (
"                              ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐\n" +
"                              │ Wx3 │     │     │ Lx2 │     │     │     │ Wx3 │     │     │     │ Lx2 │     │     │ Wx3 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Wx2 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Wx2 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Wx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Wx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Lx2 │     │     │ Wx2 │     │     │     │ Lx2 │     │     │     │ Wx2 │     │     │ Lx2 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │     │     │ Wx2 │     │     │     │     │     │ Wx2 │     │     │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Lx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Lx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Wx3 │     │     │ Lx2 │     │     │     │  ★  │     │     │     │ Lx2 │     │     │ Wx3 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Lx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Lx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │     │     │ Wx2 │     │     │     │     │     │ Wx2 │     │     │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Lx2 │     │     │ Wx2 │     │     │     │ Lx2 │     │     │     │ Wx2 │     │     │ Lx2 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Wx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Wx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Wx2 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Wx2 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Wx3 │     │     │ Lx2 │     │     │     │ Wx3 │     │     │     │ Lx2 │     │     │ Wx3 │\n" +
"                              └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")) 
                
    def testBoardWithOneWordStringRepresentation(self):
        board = Board()
        word = [Tile('CH', 5), Tile('O', 1), Tile('O', 1), Tile('S', 1), Tile(' ', 0)]
        board.putWord(word, 1, (7,3))
        self.assertEqual(board.__repr__(), (
"                              ┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐\n" +
"                              │ Wx3 │     │     │ Lx2 │     │     │     │ Wx3 │     │     │     │ Lx2 │     │     │ Wx3 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Wx2 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Wx2 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Wx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Wx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Lx2 │     │     │ Wx2 │     │     │     │ Lx2 │     │     │     │ Wx2 │     │     │ Lx2 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │     │     │ Wx2 │     │     │     │     │     │ Wx2 │     │     │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Lx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Lx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Wx3 │     │     │ [CH]│ [O] │ [O] │ [S] │ [ *]│     │     │     │ Lx2 │     │     │ Wx3 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Lx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Lx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │     │     │ Wx2 │     │     │     │     │     │ Wx2 │     │     │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Lx2 │     │     │ Wx2 │     │     │     │ Lx2 │     │     │     │ Wx2 │     │     │ Lx2 │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │     │ Wx2 │     │     │     │ Lx2 │     │ Lx2 │     │     │     │ Wx2 │     │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │     │ Wx2 │     │     │     │ Lx3 │     │     │     │ Lx3 │     │     │     │ Wx2 │     │\n" +
"                              ├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n" +
"                              │ Wx3 │     │     │ Lx2 │     │     │     │ Wx3 │     │     │     │ Lx2 │     │     │ Wx3 │\n" +
"                              └─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘"))                 
                
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
        result = player.giveTiles([6])
        self.assertEqual(result, [tile7]) 
        self.assertEqual(player.rack, [tile1, tile2, tile3, tile4, tile5, tile6])
        
    def testGiveTiles(self):
        player = Player()
        tile1 = Tile('N', 1)
        tile2 = Tile('I', 1)
        tile3 = Tile('M', 3)
        tile4 = Tile('A', 1)
        tile5 = Tile('O', 1)
        tile6 = Tile('A', 1)
        tile7 = Tile('D', 2)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        result = player.giveTiles([0, 3, 6, 4])
        self.assertEqual(result, [tile1, tile4, tile7, tile5]) 
        self.assertEqual(player.rack, [tile2, tile3, tile6])
        
    def testSumScore(self):
        player = Player()
        self.assertEqual(player.score, 0)
        player.sumScore(15)
        self.assertEqual(player.score, 15)
        player.sumScore(32)
        self.assertEqual(player.score, 47)
        
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
        
    def testHaveTilesComplex(self):
        player = Player()
        tile1 = Tile('S', 1)
        tile2 = Tile('LL', 8)
        tile3 = Tile(' ', 0)
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
        
    def testRackStringRepresentation(self):
        player = Player()
        tile1 = Tile('A', 1)
        tile2 = Tile('M', 2)
        tile3 = Tile('O', 1)
        tile4 = Tile('A', 1)
        tile5 = Tile('E', 1)
        tile6 = Tile('F', 4)
        tile7 = Tile('Y', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles) 
        self.assertEqual(player.__repr__(), 
                "                                   /║║ [A](1p.) ║ [M](2p.) ║ [O](1p.) ║ [A](1p.) ║ [E](1p.) ║ [F](4p.) ║ [Y](4p.) ║║\n" +
                "                                  |═╩╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩╝\n" + 
                "                                   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    
    def testRackWithTwoLetterTilesStringRepresentation(self):
        player = Player()
        tile1 = Tile('A', 1)
        tile2 = Tile('LL', 8)
        tile3 = Tile('O', 1)
        tile4 = Tile('CH', 5)
        tile5 = Tile('E', 1)
        tile6 = Tile('F', 4)
        tile7 = Tile('Y', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5, tile6, tile7]
        player.takeTiles(tiles)
        self.assertEqual(player.__repr__(), 
                "                                   /║║ [A](1p.) ║[LL](8p.) ║ [O](1p.) ║[CH](5p.) ║ [E](1p.) ║ [F](4p.) ║ [Y](4p.) ║║\n" +
                "                                  |═╩╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩╝\n" + 
                "                                   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    
    def testIncompleteRackStringRepresentation(self):
        player = Player()
        tile1 = Tile('A', 1)
        tile2 = Tile(' ', 0)
        tile3 = Tile('O', 1)
        tile4 = Tile('F', 4)
        tile5 = Tile('Y', 4)
        tiles = [tile1, tile2, tile3, tile4, tile5]
        player.takeTiles(tiles) 
        self.assertEqual(player.__repr__(), 
                "                                   /║║ [A](1p.) ║ [ ](0p.) ║ [O](1p.) ║ [F](4p.) ║ [Y](4p.) ║          ║          ║║\n" +
                "                                  |═╩╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩╝\n" + 
                "                                   ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    
if __name__ == '__main__':
    unittest.main()