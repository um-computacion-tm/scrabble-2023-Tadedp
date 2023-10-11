import unittest
from unittest.mock import patch
from game.models import *
from game.scrabbleGame import *

class TestScrabbleGame(unittest.TestCase):
    def testScrabbleGame(self):
        scrabbleGame = ScrabbleGame(2) 
        self.assertEqual(len(scrabbleGame.players), 2)
        self.assertEqual(len(scrabbleGame.players[0].rack), 7)
        self.assertEqual(len(scrabbleGame.players[1].rack), 7)
        self.assertEqual(scrabbleGame.currentPlayer, None)

    def testNextTurn(self):
        scrabbleGame = ScrabbleGame(2) 
        scrabbleGame.nextTurn()
        self.assertEqual(scrabbleGame.currentPlayer, scrabbleGame.players[0])
        scrabbleGame.nextTurn()
        self.assertEqual(scrabbleGame.currentPlayer, scrabbleGame.players[1])
        scrabbleGame.nextTurn()
        self.assertEqual(scrabbleGame.currentPlayer, scrabbleGame.players[0])
    
    def testGetBoard(self):
        scrabbleGame = ScrabbleGame(2)
        self.assertEqual(scrabbleGame.getBoard(), scrabbleGame.board)
    
    def testGetPlayerRack(self):
        scrabbleGame = ScrabbleGame(2)
        self.assertEqual(scrabbleGame.getPlayerRack(), scrabbleGame.currentPlayer)
    
    def testGetBagRemainingTiles(self):
        scrabbleGame = ScrabbleGame(2)
        self.assertEqual(scrabbleGame.getBagRemainingTiles(), len(scrabbleGame.tileBag.tiles))
    
    def testPlayers(self):
        scrabbleGame = ScrabbleGame(2)
        self.assertEqual(scrabbleGame.getPlayers(), scrabbleGame.players)
        
    @patch.object(Board, 'formedWords', return_value=["HELLO"])
    @patch.object(ScrabbleGame, 'validateMove', return_value="HELLO")
    @patch.object(ScrabbleGame, 'getPositions', return_value=[0, 1, 2, 3])
    @patch.object(Player, 'giveTiles', return_value=[Tile("H", 4), Tile(" ", 0), Tile("LL", 8), Tile("O", 1)])
    @patch.object(Board, 'putWord')
    @patch.object(Board, 'wordScore', return_value=26)
    @patch.object(Player, 'sumScore')
    @patch.object(Player, 'takeTiles')
    def testPlayWord(self, patchFormedWords, patchValidateMove, patchGetPositions, 
                     patchGiveTiles, patchPutWord, patchWordScore, patchSumScore, patchTakeTiles):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        scrabbleGame.playWord("HELLO", 1, (7,7))
        
    @patch.object(ScrabbleGame, 'getBagRemainingTiles', return_value=1)
    def testRaiseInsufficientTilesInBagException(self, patchGetBagRemainingTiles):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        with self.assertRaises(InsufficientTilesInBagException):    
            scrabbleGame.exchangeTiles([0, 5, 6])
            
    @patch.object(ScrabbleGame, 'getBagRemainingTiles', return_value=100)
    @patch.object(Player, 'giveTiles', return_value=[Tile("H", 4), Tile("A", 1), Tile("S", 1)])
    @patch.object(TileBag, 'take', return_value=[Tile("CH", 5), Tile(" ", 0), Tile("O", 1)])
    @patch.object(TileBag, 'put')
    @patch.object(Player, 'takeTiles')
    def testExchangeTiles(self, patchGetBagRemainingTiles, patchGiveTiles, patchTake, patchPut,
                          patchTakeTiles):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        scrabbleGame.exchangeTiles([0, 5, 6])
    
    @patch.object(Board, 'removeWordBoardTiles', return_value="HELLO")
    @patch.object(Player, 'haveTiles', return_value=True)
    @patch.object(Dictionary, 'isInDictionary', return_value=True)
    @patch.object(Board, 'wordIsInside', return_value=True)
    @patch.object(Board, 'wordIsValid', return_value=True)   
    def testValidateMove(self, patchRemoveWordBoardTiles, patchHaveTiles, patchIsInDictionary,
                         patchWordIsInside, patchWordIsValid):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        self.assertEqual(scrabbleGame.validateMove([["HELLO"]], 0, (7, 7)), "HELLO")
        
    @patch.object(Board, 'removeWordBoardTiles', return_value="HELLO")
    @patch.object(Player, 'haveTiles', return_value=False) 
    def testRaisePlayerDoesNotHaveNeededTilesException(self, patchRemoveWordBoardTiles, patchHaveTiles):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        with self.assertRaises(PlayerDoesNotHaveNeededTilesException):
            self.assertEqual(scrabbleGame.validateMove([["HELLO"]], 0, (7, 7)), "HELLO")
        
    @patch.object(Board, 'removeWordBoardTiles', return_value="HELLO")
    @patch.object(Player, 'haveTiles', return_value=True) 
    @patch.object(Dictionary, 'isInDictionary', return_value=False)
    def testRaiseWordIsNotInDictionaryException(self, patchRemoveWordBoardTiles, 
                                        patchHaveTiles, patchIsInDictionary):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        with self.assertRaises(WordIsNotInDictionaryException):
            self.assertEqual(scrabbleGame.validateMove([["HELLO"]], 0, (7, 7)), "HELLO")

    @patch.object(Board, 'removeWordBoardTiles', return_value="HELLO")
    @patch.object(Player, 'haveTiles', return_value=True) 
    @patch.object(Dictionary, 'isInDictionary', return_value=True)
    @patch.object(Board, 'wordIsInside', return_value=False)
    def testRaiseWordIsNotInsideBoardException(self, patchRemoveWordBoardTiles, 
                                        patchHaveTiles, patchIsInDictionary, patchWordIsInside):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        with self.assertRaises(WordIsNotInsideBoardException):
            self.assertEqual(scrabbleGame.validateMove([["HELLO"]], 0, (7, 7)), "HELLO")   
                     
    
    @patch.object(Board, 'removeWordBoardTiles', return_value="HELLO")
    @patch.object(Player, 'haveTiles', return_value=True) 
    @patch.object(Dictionary, 'isInDictionary', return_value=True)
    @patch.object(Board, 'wordIsInside', return_value=True)
    @patch.object(Board, 'wordIsValid', return_value=False)  
    def testRaiseWordPlacementIsNotValidException(self, patchRemoveWordBoardTiles, patchHaveTiles, 
                                        patchIsInDictionary, patchWordIsInside, patchWordIsValid):
        scrabbleGame = ScrabbleGame(2)
        scrabbleGame.nextTurn()
        with self.assertRaises(WordPlacementIsNotValidException):
            self.assertEqual(scrabbleGame.validateMove([["HELLO"]], 0, (7, 7)), "HELLO")   
                  
    def testPlayingEndsBecauseOfTiles(self):
        scrabbleGame = ScrabbleGame(3)
        scrabbleGame.nextTurn()
        scrabbleGame.tileBag.tiles = []
        scrabbleGame.currentPlayer.rack = []
        self.assertEqual(scrabbleGame.playing(5), False)   
    
    
    def testPlayingEndsBecauseOfConsecutivePasses(self):
        scrabbleGame = ScrabbleGame(3)
        scrabbleGame.nextTurn()
        self.assertEqual(scrabbleGame.playing(6), False) 
    
    def testPlayingContinues(self):   
        scrabbleGame = ScrabbleGame(4)
        scrabbleGame.nextTurn()
        self.assertEqual(scrabbleGame.playing(7), True)
                               
    def testGetPositions(self):
        scrabbleGame = ScrabbleGame(3)
        scrabbleGame.nextTurn()
        scrabbleGame.currentPlayer.rack = ([Tile('CH', 5), Tile('O', 1), Tile('A', 1), Tile(' ', 0),
                                            Tile('O', 1), Tile('S', 1), Tile(' ', 0)])
        self.assertEqual(scrabbleGame.getPositions("CHOOSE"), [0, 1, 4, 5, 3])
                                     
if __name__ == '__main__':
    unittest.main()