from game.models import *
from game.board import *
from game.dictionary import Dictionary

class WordIsNotInDictionaryException(Exception): 
    pass

class WordIsNotInsideBoardException(Exception): 
    pass

class WordPlacementIsNotValidException(Exception): 
    pass

class PlayerDoesNotHaveNeededTilesException(Exception):
    pass

class InsufficientTilesInBagException(Exception):
    pass

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
    
    def getBoard(self):
        return self.board
    
    def getPlayerRack(self):
        return self.currentPlayer
    
    def getBagRemainingTiles(self):
        return len(self.tileBag.tiles)
    
    def getPlayers(self):
        return self.players
    
    def playWord(self, mainWord: str, increasingCoordinate: int, firstTilePosition: tuple):
        words = self.board.formedWords(mainWord, increasingCoordinate, firstTilePosition)
        cutMainWord = self.validateMove(words, increasingCoordinate, firstTilePosition)
        cutMainWordCopy = cutMainWord
        positions = self.getPositions(cutMainWord)
        newTiles = self.currentPlayer.giveTiles(positions)
        doubleLettersCounter = 0
        for i in range(len(newTiles)):
            doubleLetterTile = False
            
            if len(cutMainWordCopy[i:]) > 2 and (cutMainWordCopy[i : i+2] == "LL" or cutMainWordCopy[i : i+2] == "RR" or cutMainWordCopy[i : i+2] == "CH"):
                doubleLettersCounter += 1
                doubleLetterTile = True
                
            if newTiles[i].value == 0:
                if doubleLetterTile:
                    newTiles[i].letter = cutMainWordCopy[i + doubleLettersCounter - 1: i + doubleLettersCounter + 1]
                else:    
                    newTiles[i].letter = cutMainWordCopy[i + doubleLettersCounter]
                
        self.board.putWord(newTiles, increasingCoordinate, firstTilePosition)
        total = 0
        for word in words:
            total += self.board.wordScore(len(word[0]), increasingCoordinate, firstTilePosition)
        self.currentPlayer.sumScore(total)
        self.currentPlayer.takeTiles(self.tileBag.take(len(positions)))
        
    def exchangeTiles(self, positions: list):
        if len(positions) > self.getBagRemainingTiles():
            raise InsufficientTilesInBagException("La bolsa tiene fichas insuficientes.")
        playerTiles = self.currentPlayer.giveTiles(positions)
        bagTiles = self.tileBag.take(len(positions))
        self.tileBag.put(playerTiles)
        self.currentPlayer.takeTiles(bagTiles)
        
    def validateMove(self, words: list, increasingCoordinate: int, firstTilePosition: tuple):
        mainWord = words[0][0]
        cutMainWord = self.board.removeWordBoardTiles(mainWord, increasingCoordinate, firstTilePosition)
        if not self.currentPlayer.haveTiles(cutMainWord):
            raise PlayerDoesNotHaveNeededTilesException("No tiene las fichas necesarias para jugar " + 
                mainWord.lower() + ".")
        for word in words:
            if not Dictionary.isInDictionary(word[0]):
                raise WordIsNotInDictionaryException("La palabra " + word[0].lower() + 
                                                     " no existe en el diccionario.")
        if not self.board.wordIsInside(mainWord, increasingCoordinate, firstTilePosition):
            raise WordIsNotInsideBoardException("La palabra " + mainWord.lower() + 
                " puesta a partir de la posición (" + str(firstTilePosition[0]) + "," +  
                str(firstTilePosition[1]) + ") no entra en el tablero.")
        if not self.board.wordIsValid(mainWord, increasingCoordinate, firstTilePosition):
            raise WordPlacementIsNotValidException("El posicionamiento de la palabra " + mainWord.lower() + 
                " es inválido.")
        return cutMainWord
    
    def playing(self, consecutivePasses):
        if len(self.currentPlayer.rack) < 1 and len(self.tileBag.tiles) < 1:
            return False 
        
        if consecutivePasses == 2 * len(self.players):
            return False    
        return True
    
    def getPositions(self, cutMainWord):
        positions = [] 
        while len(cutMainWord) > 0:
            letterNotFound = True
            cutMainWord, letter = self.getLetter(cutMainWord)
                
            for j in range(len(self.currentPlayer.rack)):
                if letter == self.currentPlayer.rack[j].letter and not j in positions:
                    positions.append(j)
                    letterNotFound = False
                    break
            
            if letterNotFound:
                for j in range(len(self.currentPlayer.rack)):
                    if self.currentPlayer.rack[j].letter == " ":
                        positions.append(j)
                        break
        return positions
    
    def getLetter(self, cutMainWord: str):
        if len(cutMainWord) > 2 and (cutMainWord[0 : 2] == "LL" or cutMainWord[0 : 2] == "RR" or cutMainWord[0 : 2] == "CH"):
            letter = cutMainWord[0 : 2]
            cutMainWord = cutMainWord[2:]
        else:
            letter = cutMainWord[0]
            cutMainWord = cutMainWord[1:]
        return cutMainWord, letter    