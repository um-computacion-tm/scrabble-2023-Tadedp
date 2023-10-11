import unittest
from unittest.mock import patch
from game.models import *
from game.scrabbleCli import *
from game.main import *

class TestMainDictionary(unittest.TestCase):
    @patch.object(ScrabbleCli, 'getPlayersCount', return_value=2)
    @patch.object(ScrabbleGame, 'nextTurn')
    @patch.object(ScrabbleGame, 'playing', return_value=True)
    @patch.object(ScrabbleGame, 'getBoard')
    @patch.object(ScrabbleGame, 'getPlayerRack')
    @patch.object(ScrabbleCli, 'getPlayerMove', return_value=1)
    @patch.object(ScrabbleCli, 'getWordInputs', return_value=('HELLO', 0, (7, 7)))
    @patch.object(ScrabbleGame, 'playWord')   
    @patch.object(ScrabbleGame, 'getPlayers', return_value=(Player(), Player()))
    @patch.object(ScrabbleCli, 'getKeepPlayingInputs', return_value=False)
    @patch.object(ScrabbleCli, 'getFinalScores', return_value=[22, 24])
    @patch('builtins.print')
    def testClient(self, patchGetPlayersCount, patchnextTurn, patchplaying, patchgetBoard, 
                   patchgetPlayerRack, patchgetPlayerMove, patchgetWordInputs, patchplayWord,
                   patchgetPlayers, patchgetKeepPlayingInputs, patchgetFinalScores, patchPrint):
        main()
        
if __name__ == '__main__':
    unittest.main()