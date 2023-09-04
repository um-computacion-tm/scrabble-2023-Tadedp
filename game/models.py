import random

class EmptyBagException(Exception):
    pass

class OccupiedSquareException(Exception):
    pass

class MissingTileInRackException(Exception):
    pass

class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value
        
class TileBag:
    def __init__(self):
        tileValues = [('', 0, 2), ('A', 1, 12), ('E', 1, 12), ('O', 1, 9), ('I', 1, 6), 
                      ('S', 1, 6), ('N', 1, 5), ('R', 1, 5), ('U', 1, 5), ('L', 1, 4), 
                      ('T', 1, 4), ('D', 2, 5), ('G', 2, 2), ('C', 3, 4), ('B', 3, 2), 
                      ('M', 3, 2), ('P', 3, 2), ('H', 4, 2), ('F', 4, 1), ('V', 4, 1), 
                      ('Y', 4, 1), ('CH', 5, 1), ('Q', 5, 1), ('J', 8, 1), ('LL', 8, 1), 
                      ('Ñ', 8, 1), ('RR', 8, 1), ('X', 8, 1), ('Z', 10, 1)]
        
        self.tiles = [Tile(tile[0], tile[1]) for tile in tileValues for _ in range(tile[2])]
        random.shuffle(self.tiles)
        
    def take(self, count):
        tiles = [] 
        
        for i in range(count):
            if len(self.tiles) == 0:
                if i == 0:
                    raise EmptyBagException("The tile bag is empty.")
                else:
                    break
            tiles.append(self.tiles.pop())
        
        return tiles
    
    def put(self, tiles):
        self.tiles.extend(tiles)
    
class Square:
    def __init__(self, multiplier = 1, bonusType = 'L'):
        self.multiplier = multiplier
        self.bonusType = bonusType
        self.tile = None
    
    def putTile(self, tile):
        if self.tile != None:
            raise OccupiedSquareException("Square already occupied.")
        else:
            self.tile = tile
        
    def squareValue(self):
        value = 0
        
        if self.tile != None:
            value = self.tile.value
            if self.bonusType == "L":
                value = value * self.multiplier
        
        return value
    
    def resetBonus(self):
        self.multiplier = 1
        self.bonusType = 'L'

class Board:
    def __init__(self):
        self.board = [[Square() for _ in range(15)] for _ in range(15)]
        
        coordinates = [(0,0), (0,7), (7,0)]
        self.putBonuses(coordinates, (3, 'W'))

        coordinates = [(1,1), (2,2), (3,3), (4,4)]
        self.putBonuses(coordinates, (2, 'W'))
        
        coordinates = [(5,1), (5,5), (1,5)]
        self.putBonuses(coordinates, (3, 'L'))
        
        coordinates = [(0,3), (3,0), (2,6), (6,2), (7, 3), (3, 7), (6, 6)]
        self.putBonuses(coordinates, (2, 'L'))
    
    def putBonuses(self, coordinates, bonus):
        for coordinate in coordinates:
            self.board[coordinate[0]][coordinate[1]] = (
                self.board[coordinate[0]][14 - coordinate[1]]) = (
                self.board[14 - coordinate[0]][coordinate[1]]) = (
                self.board[14 - coordinate[0]] [14 - coordinate[1]]) = Square(bonus[0], bonus[1])
 
    def putWord(self, newTiles = [], increasingCoordinate = 0, firstTilePosition = (0, 0), boardTilesPositions = []):
        lenWord = len(newTiles) + len(boardTilesPositions) 
        for i in range(lenWord):
            skipTile = False
            if increasingCoordinate == 0:
                for j in range(len(boardTilesPositions)):
                    if firstTilePosition[0] + i == boardTilesPositions[j][0] and firstTilePosition[1] == boardTilesPositions[j][1]:
                        boardTilesPositions.pop(j)
                        skipTile = True
                        break
                if skipTile:
                    continue
                square = self.board[firstTilePosition[0] + i][firstTilePosition[1]]
            
            else:
                for j in range(len(boardTilesPositions)):
                    if firstTilePosition[0] == boardTilesPositions[j][0] and firstTilePosition[1] + i == boardTilesPositions[j][1]:    
                        boardTilesPositions.pop(j)
                        skipTile = True
                        break
                if skipTile:
                    continue
                square = self.board[firstTilePosition[0]][firstTilePosition[1] + i]
        
            try:
                square.putTile(newTiles.pop(0))
            except OccupiedSquareException:
                raise OccupiedSquareException("Square already occupied.")
            
    def wordScore(self, lenWord, increasingCoordinate = 0, firstTilePosition = (0, 0)):
        wordMultiplier = 1
        score = 0
        for i in range(firstTilePosition[increasingCoordinate], firstTilePosition[increasingCoordinate] + lenWord):
            if increasingCoordinate == 0:
                square = self.board[i][firstTilePosition[1]]
            else:
                square = self.board[firstTilePosition[0]][i]
            
            if square.bonusType == 'W':
                wordMultiplier = wordMultiplier * square.multiplier 
            
            score = score + square.squareValue()
            
            if square.multiplier > 1:
                square.resetBonus()
        
        score = wordMultiplier * score
        return score             
    
class Player:
    def __init__(self):
        self.rack = []
        self.score = 0
    
    def takeTiles(self, tiles):
        for tile in tiles:
            self.rack.append(tile)
            
    def giveTiles(self, letters):
        rackBackUp = self.rack.copy()
        tiles = []
        for i in range(len(letters)):
            letterIndex = -1
            for j in range(7 - i):
                if self.rack[j].letter == letters[i].upper(): 
                    letterIndex = j
                    break
            
            if letterIndex == -1:
                self.rack = rackBackUp
                raise MissingTileInRackException(letters[i] + " letter missing in rack.")
            else:
                tiles.append(self.rack.pop(letterIndex))
        return tiles