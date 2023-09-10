import unittest
from game.scrabbleGame import ScrabbleGame

class TestTile(unittest.TestCase):
    def testScrabbleGame(self):
        scrabbleGame = ScrabbleGame(2) 
        self.assertEqual(len(scrabbleGame.players), 2)
        self.assertEqual(len(scrabbleGame.players[0].rack), 7)
        self.assertEqual(len(scrabbleGame.players[1].rack), 7)
        self.assertEqual(scrabbleGame.currentPlayer, None)

if __name__ == '__main__':
    unittest.main()