from game.models import *

class ScrabbleGame:
    def __init__(self, playersCount: int):
        self.board = Board()
        self.tileBag = TileBag()
        self.players:list[Player] = []
        for i in range(playersCount):
            self.players.append(Player())
            playerTiles = self.tileBag.take(7)
            self.players[i].takeTiles(playerTiles)
        
        self.currentPlayer = None