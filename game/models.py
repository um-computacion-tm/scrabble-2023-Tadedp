import random

class Tile:
    def __init__(self, letter: str, value: int):
        self.letter = letter
        self.value = value
    
    def __repr__(self):
        return str("[" + self.letter + "](" + str(self.value) + "p.)")
        
class TileBag:
    def __init__(self):
        tileValues = [(' ', 0, 2), ('A', 1, 12), ('E', 1, 12), ('O', 1, 9), ('I', 1, 6), 
                      ('S', 1, 6), ('N', 1, 5), ('R', 1, 5), ('U', 1, 5), ('L', 1, 4), 
                      ('T', 1, 4), ('D', 2, 5), ('G', 2, 2), ('C', 3, 4), ('B', 3, 2), 
                      ('M', 3, 2), ('P', 3, 2), ('H', 4, 2), ('F', 4, 1), ('V', 4, 1), 
                      ('Y', 4, 1), ('CH', 5, 1), ('Q', 5, 1), ('J', 8, 1), ('LL', 8, 1), 
                      ('Ñ', 8, 1), ('RR', 8, 1), ('X', 8, 1), ('Z', 10, 1)]
        
        self.tiles = [Tile(tile[0], tile[1]) for tile in tileValues for _ in range(tile[2])]
        random.shuffle(self.tiles)
        
    def take(self, count: int):
        return [self.tiles.pop() for _ in range(count)]
    
    def put(self, tiles : list):
        self.tiles.extend(tiles)
        random.shuffle(self.tiles)
    
class Square:
    def __init__(self, multiplier: int = 1, bonusType: str = 'L'):
        self.multiplier = multiplier
        self.bonusType = bonusType
        self.tile = None
    
    def putTile(self, tile: Tile):
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
    
    def __repr__(self):
        if self.tile == None:
            if self.bonusType == "W":
                square = "Wx" + str(self.multiplier) 
            else:
                if self.multiplier > 1:
                    square = "Lx" + str(self.multiplier) 
                else:
                    square = "   "
        else:
            tileEnd = self.tile.__repr__().index("]")
            if self.tile.value > 0:
                square = self.tile.__repr__()[0 : tileEnd + 1] 
            else:
                square = self.tile.__repr__()[0 : tileEnd] + "*" + self.tile.__repr__()[tileEnd]
        return square
        
class Player:
    def __init__(self):
        self.rack = []
        self.score = 0
    
    def takeTiles(self, tiles: list):
        for tile in tiles:
            self.rack.append(tile)
            
    def giveTiles(self, positions: list):
        tiles = []
        for i in range(len(positions)):
            tiles.append(self.rack.pop(positions[i]))
            for j in range(len(positions)):
                if positions[i] < positions[j]:
                    positions[j] -= 1
        return tiles
   
    def haveTiles(self, word: str):
        usedTiles = []
        while len(word) > 0:
            word, letter = self.getLetter(word)
                
            if not self.isLetterInRack(letter, usedTiles):
                hasBlankTile = False
                for i in range(len(self.rack)):
                    if self.rack[i].letter == " " and usedTiles.count(i) < 1:
                        hasBlankTile = True
                        usedTiles.append(i)
                        break
                if not hasBlankTile:
                    return False
        return True     
    
    def getLetter(self, word: str):
        if len(word) > 1:
            if word[0 : 2].upper() == "LL" or word[0 : 2].upper() == "RR" or word[0 : 2].upper() == "CH":
                letter =  word[0 : 2].upper()
                word = word[2:]
            else:
                letter = word[0].upper()
                word = word[1:]
        else:
            letter = word[0].upper()    
            word = word[1:]
        return word, letter
    
    def isLetterInRack(self, letter: str, usedTiles: list):
        letterInRack = False
        for i in range(len(self.rack)):
            if letter == self.rack[i].letter and usedTiles.count(i) < 1:
                letterInRack = True
                usedTiles.append(i)
        return letterInRack
    
    def sumScore(self, score: int):
        self.score += score
    
    def __repr__(self):
        spaces = "                                  " 
        rack = spaces + " /║║"
        for i in range(7):
            if len(self.rack) < 7 and i >= len(self.rack):
                rack = rack + "          ║"
            else:
                if len(self.rack[i].letter) > 1:
                    rack = rack + str(self.rack[i]) + " ║"
                else:        
                    rack = rack + " " + str(self.rack[i]) + " ║"
        rack = (rack + 
                "║\n" + spaces + 
                "|═╩╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩══════════╩╝\n" +
                spaces +
                " ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")  
        return rack