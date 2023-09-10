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
    
    def nextTurn(self):
        if self.currentPlayer is None or self.currentPlayer == self.players[-1]:
            self.currentPlayer = self.players[0]
        else:
            index = self.players.index(self.currentPlayer) + 1
            self.currentPlayer = self.players[index]