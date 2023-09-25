import unittest
from game.scrabbleGame import ScrabbleGame

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
        
if __name__ == '__main__':
    unittest.main()