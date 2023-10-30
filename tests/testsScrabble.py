import unittest
from unittest.mock import patch
from game.models import (
    Tile, 
    TileBag,
    Square,
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