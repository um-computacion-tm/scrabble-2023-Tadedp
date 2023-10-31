import unittest
from unittest.mock import patch
from game.scrabbleCli import ScrabbleCli
from game.models import *
from game.scrabbleGame import *

class TestScrabbleClient(unittest.TestCase):
    @patch('builtins.input', return_value='3')
    def testGetPlayersCount(self, patchInput):
        self.assertEqual(ScrabbleCli.getPlayersCount(), 3)

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['10', '2'])
    def testGetPlayersCountWrongInput(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getPlayersCount(), 2)

    @patch('builtins.input', return_value='1')
    def testGetPlayerMove(self, patchInput):
        self.assertEqual(ScrabbleCli.getPlayerMove(), 1)
        
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['0', '3'])
    def testGetPlayerMoveWrongInput(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getPlayerMove(), 3)
        
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['TEAR', 'H', '8', '8'])
    def testGetWordInputs(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getWordInputs(), ('TEAR', 1, (7, 7)))

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['5', 'TEAR', 'V', '15', '15'])
    def testGetWordInputsWrongWord(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getWordInputs(), ('TEAR', 0, (14, 14)))

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['TEAR', '0', 'TEAR', 'V', '1', '1'])
    def testGetWordInputsWrongOrientation(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getWordInputs(), ('TEAR', 0, (0, 0)))
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['5', '7', '1', 'T'])
    def testGetExchangeInputs(self, patchPrint, patchInput):
        bagLen = 100
        player = Player()
        player.rack = ([Tile('CH', 5), Tile('O', 1), Tile('A', 1), Tile(' ', 0), Tile('O', 1), 
                       Tile('S', 1), Tile(' ', 0)])
        self.assertEqual(ScrabbleCli.getExchangeInputs(bagLen, player), ([4, 6, 0]))
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['0'])
    def testGetExchangeInputsFullRackInput(self, patchPrint, patchInput):
        bagLen = 100
        player = Player()
        player.rack = ([Tile('CH', 5), Tile('O', 1), Tile('A', 1), Tile(' ', 0), Tile('O', 1), 
                       Tile('S', 1)])
        self.assertEqual(ScrabbleCli.getExchangeInputs(bagLen, player), ([0, 1, 2, 3, 4, 5]))

    @patch('builtins.print')
    @patch('builtins.input', side_effect=['7', '6', '5', '4', '3', '2', '1'])
    def testGetExchangeInputsAllInputs(self, patchPrint, patchInput):
        bagLen = 100
        player = Player()
        player.rack = ([Tile('CH', 5), Tile('O', 1), Tile('A', 1), Tile(' ', 0), Tile('O', 1), 
                       Tile('S', 1), Tile(' ', 0)])
        self.assertEqual(ScrabbleCli.getExchangeInputs(bagLen, player), ([6, 5, 4, 3, 2, 1, 0]))
        
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['A', '2', '10', '5', 'T'])
    def testGetExchangeInputsWrongInputs(self, patchPrint, patchInput):
        bagLen = 100
        player = Player()
        player.rack = ([Tile('CH', 5), Tile('O', 1), Tile('A', 1), Tile(' ', 0), Tile('O', 1), 
                       Tile('S', 1), Tile(' ', 0)])
        self.assertEqual(ScrabbleCli.getExchangeInputs(bagLen, player), ([1, 4]))
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['S'])
    def testKeepPlaying(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getKeepPlayingInputs(), True)
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['N'])
    def testNotKeepPlaying(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getKeepPlayingInputs(), False)
    
    @patch('builtins.print')
    @patch('builtins.input', side_effect=['1', 'A', 'S'])
    def testGetKeepPlayingWrongInputs(self, patchPrint, patchInput):
        self.assertEqual(ScrabbleCli.getKeepPlayingInputs(), True)
    
    def testGetFinalScores(self):
        player1 = Player()
        player1.score = 22
        player1.rack = []
        
        player2 = Player()
        player2.score = 18
        player2.rack = ([Tile('LL', 8), Tile('S', 1), Tile('A', 1), Tile('P', 3), Tile('Ñ', 8), 
                       Tile(' ', 0), Tile('O', 1)])
        players = [player1, player2]
        self.assertEqual(ScrabbleCli.getFinalScores(players), [44, -4])
    
    @patch.object(ScrabbleCli, 'getPlayersCount', return_value=2)
    @patch.object(ScrabbleGame, 'nextTurn')
    @patch.object(ScrabbleGame, 'playing', return_value=True)
    @patch.object(ScrabbleGame, 'getBoard')
    @patch.object(ScrabbleGame, 'getPlayerRack')
    @patch.object(ScrabbleCli, 'getPlayerMove', return_value=1)
    @patch.object(ScrabbleCli, 'getWordInputs', return_value=('HELLO', 0, (7, 7)))
    @patch.object(ScrabbleGame, 'playWord')   
    @patch.object(ScrabbleGame, 'getPlayers', return_value=[Player(), Player()])
    @patch.object(ScrabbleCli, 'getKeepPlayingInputs', return_value=False)
    @patch.object(ScrabbleCli, 'getFinalScores', return_value=[22, 24])
    @patch('builtins.print')
    def testCliPutWord(self, patchGetPlayersCount, patchnextTurn, patchplaying, patchgetBoard, 
                   patchgetPlayerRack, patchgetPlayerMove, patchgetWordInputs, patchplayWord,
                   patchgetPlayers, patchgetKeepPlayingInputs, patchgetFinalScores, patchPrint):
        client = ScrabbleCli()
        client.client()
        
    @patch.object(ScrabbleCli, 'getPlayersCount', return_value=2)
    @patch.object(ScrabbleGame, 'nextTurn')
    @patch.object(ScrabbleGame, 'playing', return_value=True)
    @patch.object(ScrabbleGame, 'getBoard')
    @patch.object(ScrabbleGame, 'getPlayerRack')
    @patch.object(ScrabbleCli, 'getPlayerMove', return_value=2)
    @patch.object(ScrabbleCli, 'getExchangeInputs', return_value=([1, 2, 3]))
    @patch.object(ScrabbleGame, 'exchangeTiles') 
    @patch.object(ScrabbleGame, 'getPlayers', return_value=[Player(), Player()])
    @patch.object(ScrabbleCli, 'getKeepPlayingInputs', return_value=False)
    @patch.object(ScrabbleCli, 'getFinalScores', return_value=[22, 24])
    @patch('builtins.print')
    def testCliExchangeTiles(self, patchGetPlayersCount, patchnextTurn, patchplaying, patchgetBoard, 
                   patchgetPlayerRack, patchgetPlayerMove, patchgetExchangeInputs, patchexchangeTiles,
                   patchgetPlayers, patchgetKeepPlayingInputs, patchgetFinalScores, patchPrint):
        client = ScrabbleCli()
        client.client()

    @patch.object(ScrabbleCli, 'getPlayersCount', return_value=2)
    @patch.object(ScrabbleGame, 'nextTurn')
    @patch.object(ScrabbleGame, 'playing', return_value=True)
    @patch.object(ScrabbleGame, 'getBoard')
    @patch.object(ScrabbleGame, 'getPlayerRack')
    @patch.object(ScrabbleCli, 'getPlayerMove', return_value=3)
    @patch.object(ScrabbleGame, 'getPlayers', return_value=[Player(), Player()])
    @patch.object(ScrabbleCli, 'getKeepPlayingInputs', return_value=False)
    @patch.object(ScrabbleCli, 'getFinalScores', return_value=[22, 24])
    @patch('builtins.print')
    def testCliPass(self, patchGetPlayersCount, patchnextTurn, patchplaying, patchgetBoard, 
                   patchgetPlayerRack, patchgetPlayerMove, ppatchgetPlayers, 
                   patchgetKeepPlayingInputs, patchgetFinalScores, patchPrint):
        client = ScrabbleCli()
        client.client()   
        
if __name__ == '__main__':
    unittest.main()