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
                return "Wx" + str(self.multiplier)
            else:
                if self.multiplier > 1:
                    return "Lx" + str(self.multiplier)
                else:
                    return "   "
        else:
            tileEnd = self.tile.__repr__().index("]")
            if self.tile.value > 0:
                return self.tile.__repr__()[0 : tileEnd + 1]
            else:
                return self.tile.__repr__()[0 : tileEnd] + "*" + self.tile.__repr__()[tileEnd]
 
class Board:
    def __init__(self):
        self.board = [[Square() for _ in range(15)] for _ in range(15)]
        
        coordinates = [(0,0), (0,7), (7,0)]
        self.putBonuses(coordinates, (3, 'W'))

        coordinates = [(1,1), (2,2), (3,3), (4,4), (7,7)]
        self.putBonuses(coordinates, (2, 'W'))
        
        coordinates = [(5,1), (5,5), (1,5)]
        self.putBonuses(coordinates, (3, 'L'))
        
        coordinates = [(0,3), (3,0), (2,6), (6,2), (7, 3), (3, 7), (6, 6)]
        self.putBonuses(coordinates, (2, 'L'))
    
    def putBonuses(self, positions: list, bonus: tuple):
        for coordinate in positions:
            self.board[coordinate[0]][coordinate[1]] = Square(bonus[0], bonus[1])
            self.board[coordinate[0]][14 - coordinate[1]] = Square(bonus[0], bonus[1])
            self.board[14 - coordinate[0]][coordinate[1]] = Square(bonus[0], bonus[1])
            self.board[14 - coordinate[0]] [14 - coordinate[1]] = Square(bonus[0], bonus[1])
    
    def putWord(self, newTiles: list, increasingCoordinate: int, firstTilePosition: tuple):
        actualPosition = [firstTilePosition[0], firstTilePosition[1]]
        while len(newTiles) > 0:
            square = self.board[actualPosition[0]][actualPosition[1]]
            if square.tile != None:
                actualPosition[increasingCoordinate] += 1
                continue
            square.putTile(newTiles.pop(0))
            actualPosition[increasingCoordinate] += 1
    
    def wordScore(self, lenWord: int, increasingCoordinate: int, firstTilePosition: tuple):
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
    
    def wordIsInside(self, word: str, increasingCoordinate: int, firstTilePosition: tuple):  
        wordLen = len(word) - 1
        if firstTilePosition[0] > 14 or firstTilePosition[0] < 0 or firstTilePosition[1] > 14 or firstTilePosition[1] < 0:
            return False
        
        if firstTilePosition[increasingCoordinate] + wordLen > 14:
            return False 
        
        return True       
    
    def wordIsValid(self, word: str, increasingCoordinate: int, firstTilePosition: tuple):
        if self.board[7][7].tile == None:
            return self.validFirstMove(word, increasingCoordinate, firstTilePosition)
        else:
            return self.validNotInitialMove(word, increasingCoordinate, firstTilePosition)
                
    def validFirstMove(self, word: str, increasingCoordinate: int, firstTilePosition: tuple):
        wordLen = len(word) - 1
        
        if wordLen < 1:
            return False
        
        if firstTilePosition[increasingCoordinate] > 7 or firstTilePosition[increasingCoordinate] + wordLen < 7: 
            return False
        
        if firstTilePosition[increasingCoordinate - 1] != 7:
            return False
    
        return True
    
    def validNotInitialMove(self, word: str, increasingCoordinate: int, firstTilePosition: tuple):
        useBoardTile = False
        adjacentToPlayedWord = False
        actualPosition = [firstTilePosition[0], firstTilePosition[1]]
        
        if actualPosition[increasingCoordinate] > 0:
            actualPosition[increasingCoordinate] -= 1
            if self.board[actualPosition[0]][actualPosition[1]].tile != None :
                return False

            actualPosition[increasingCoordinate] += 1
        
        while len(word) > 0:
            if len(word) > 2 and (word[0 : 2] == "LL" or word[0 : 2] == "RR" or word[0 : 2] == "CH"):
                letter = word[0 : 2]
                word = word[2:]
            else:
                letter = word[0]
                word = word[1:]
                
            actualSquare = self.board[actualPosition[0]][actualPosition[1]]
           
            if actualSquare.tile != None:
                if actualSquare.tile.letter != letter:
                    return False
                useBoardTile = True
            
            if actualPosition[increasingCoordinate - 1] > 0:
                actualPosition[increasingCoordinate - 1] -= 1
                if self.board[actualPosition[0]][actualPosition[1]].tile != None:
                    adjacentToPlayedWord = True
                actualPosition[increasingCoordinate - 1] += 1
                
            if actualPosition[increasingCoordinate - 1] < 14:
                actualPosition[increasingCoordinate - 1] += 1
                if self.board[actualPosition[0]][actualPosition[1]].tile != None:
                    adjacentToPlayedWord = True
                actualPosition[increasingCoordinate - 1] -= 1
            
            if useBoardTile or adjacentToPlayedWord:
                return True
            
            actualPosition[increasingCoordinate] += 1
        return False
    
    def formedWords(self, word: str, increasingCoordinate: int, firstTilePosition: tuple):
        words = [[word]]         
        actualPosition = [firstTilePosition[0], firstTilePosition[1]]
        for i in range(len(word)):
            words[0].append(self.board[actualPosition[0]][actualPosition[1]])
            if self.board[actualPosition[0]][actualPosition[1]].tile != None:
                actualPosition[increasingCoordinate] += 1
                continue
            letterPosition = actualPosition.copy()
            searchAfterTile = False
            if actualPosition[increasingCoordinate - 1] > 0:
                actualPosition[increasingCoordinate - 1] -= 1
                if self.board[actualPosition[0]][actualPosition[1]].tile != None :
                    words.append(self.searchExtraWord(increasingCoordinate - 1, letterPosition, word[i]))
                else:
                    searchAfterTile = True
                actualPosition[increasingCoordinate - 1] += 1

            if actualPosition[increasingCoordinate - 1] < 14 and searchAfterTile:
                actualPosition[increasingCoordinate - 1] += 1
                if self.board[actualPosition[0]][actualPosition[1]].tile != None :
                    words.append(self.searchExtraWord(increasingCoordinate - 1, letterPosition, word[i]))
                actualPosition[increasingCoordinate - 1] -= 1
            
            actualPosition[increasingCoordinate] += 1
        return words
        
    def searchExtraWord(self, increasingCoordinate: int, letterPosition: tuple, letter: str):
        actualPosition = letterPosition.copy()
        while actualPosition[increasingCoordinate] > 0:
            actualPosition[increasingCoordinate] -= 1
            if self.board[actualPosition[0]][actualPosition[1]].tile != None :
                continue
            else:
                actualPosition[increasingCoordinate] += 1
                break
            
        if actualPosition == letterPosition:
            word = [letter]
        else:
            word = [self.board[actualPosition[0]][actualPosition[1]].tile.letter]
        word.append(self.board[actualPosition[0]][actualPosition[1]])
        
        while actualPosition[increasingCoordinate] < 14:    
            actualPosition[increasingCoordinate] += 1
            if self.board[actualPosition[0]][actualPosition[1]].tile != None :
                word[0] += self.board[actualPosition[0]][actualPosition[1]].tile.letter
                word.append(self.board[actualPosition[0]][actualPosition[1]])
                continue
            else:
                if actualPosition == letterPosition:
                    word[0] += letter 
                    word.append(self.board[actualPosition[0]][actualPosition[1]])
                    continue   
                break
        return word

    def removeWordBoardTiles(self, word: str, increasingCoordinate: int, firstTilePosition: tuple): 
        lenWord = len(word)
        lettersCounter = 0
        boardTilescounter = 0
        actualPosition = [firstTilePosition[0], firstTilePosition[1]]
        while lettersCounter < lenWord:
            if self.board[actualPosition[0]][actualPosition[1]].tile != None:
                if len(self.board[actualPosition[0]][actualPosition[1]].tile.letter) > 1:
                    word = word[0 : lettersCounter - boardTilescounter] + word[ lettersCounter + 2 - boardTilescounter:]
                else:    
                    word = word[0 : lettersCounter - boardTilescounter] + word[ lettersCounter + 1 - boardTilescounter:]
                boardTilescounter += 1  
            else:
                if len(word[lettersCounter:]) > 2 and (word[lettersCounter : lettersCounter+2] == "LL" or word[lettersCounter : lettersCounter+2] == "RR" or word[lettersCounter : lettersCounter+2] == "CH"):
                    lettersCounter += 2
                else:
                    lettersCounter += 1
            actualPosition[increasingCoordinate] += 1
        return word

    def __repr__(self):
        spaces = "                              "
        board = (spaces +
            "┌─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┬─────┐\n")
        
        for i in range(15):    
            board = board + spaces + "│" 
            for j in range(15):
                if i == 7 and j == 7 and self.board[i][j].tile == None:
                    board = board + "  ★  │"
                else:    
                    board = (board + (self.board[i][j].__repr__()).center(5, " ") + "│")
                if j == 14:
                    board = board + "\n"
            if i != 14:
                board = (board + spaces + 
            "├─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┼─────┤\n")
            else:
                board = (board + spaces + 
            "└─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┴─────┘")
        return board
        
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
                
            letterInRack = False
            for i in range(len(self.rack)):
                if letter == self.rack[i].letter and usedTiles.count(i) < 1:
                    letterInRack = True
                    usedTiles.append(i)
                    break
                
            if letterInRack == False:
                hasBlankTile = False
                for i in range(len(self.rack)):
                    if self.rack[i].letter == " " and usedTiles.count(i) < 1:
                        hasBlankTile = True
                        usedTiles.append(i)
                        break
                if not hasBlankTile:
                    return False
        return True     
                
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