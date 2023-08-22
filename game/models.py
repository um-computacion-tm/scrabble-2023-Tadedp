import random

class EmptyBagException(Exception):
    pass

class OccupiedSquareException(Exception):
    pass

class Tile:
    def __init__(self, letter, value):
        self.letter = letter
        self.value = value
        
class TileBag:
    def __init__(self):
        self.tiles = [
            Tile('', 0),
            Tile('', 0),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('A', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('E', 1),
            Tile('I', 1),
            Tile('I', 1),
            Tile('I', 1),
            Tile('I', 1),
            Tile('I', 1),
            Tile('I', 1),
            Tile('L', 1),
            Tile('L', 1),
            Tile('L', 1),
            Tile('L', 1),
            Tile('N', 1),
            Tile('N', 1),
            Tile('N', 1),
            Tile('N', 1),
            Tile('N', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('O', 1),
            Tile('R', 1),
            Tile('R', 1),
            Tile('R', 1),
            Tile('R', 1),
            Tile('R', 1),
            Tile('S', 1),
            Tile('S', 1),
            Tile('S', 1),
            Tile('S', 1),
            Tile('S', 1),
            Tile('S', 1),
            Tile('T', 1),
            Tile('T', 1),
            Tile('T', 1),
            Tile('T', 1),
            Tile('U', 1),
            Tile('U', 1),
            Tile('U', 1),
            Tile('U', 1),
            Tile('U', 1),
            Tile('D', 2),
            Tile('D', 2),
            Tile('D', 2),
            Tile('D', 2),
            Tile('D', 2),
            Tile('G', 2),
            Tile('G', 2),
            Tile('B', 3),
            Tile('B', 3),
            Tile('C', 3),
            Tile('C', 3),
            Tile('C', 3),
            Tile('C', 3),
            Tile('M', 3),
            Tile('M', 3),
            Tile('P', 3),
            Tile('P', 3),
            Tile('F', 4),
            Tile('H', 4),
            Tile('H', 4),
            Tile('V', 4),
            Tile('Y', 4),
            Tile('CH', 5),
            Tile('Q', 5),
            Tile('J', 8),
            Tile('LL', 8),
            Tile('Ñ', 8),
            Tile('RR', 8),
            Tile('X', 8),
            Tile('Z', 10)
        ]
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


class Board:
    def __init__(self):
        self.board = [
            [   
                [Square(multiplier = 3, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2),None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3, bonusType = 'W'), None]
                ], 
            [   
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None]
                ],
            [
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None] 
                ],
            [
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None]
                ],
            [
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None]
                ],
            [
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None]  
                ],
            [
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None]   
                ],
            [
                [Square(multiplier = 3, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3, bonusType = 'W'), None]   
                ],
            [
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None]   
                ],
            [
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None]   
                ],
            [
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(), None]   
                ],
            [
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None]
                ],
            [
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None] 
                ],
            [
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2, bonusType = 'W'), None],
                [Square(), None]
                ],
            [
                [Square(multiplier = 3, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3, bonusType = 'W'), None],
                [Square(), None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 2),None],
                [Square(), None],
                [Square(), None],
                [Square(multiplier = 3, bonusType = 'W'), None]
                ] 
        ]
    
    def put(self, tile, position = (0, 0)):
        if self.board[position[0]][position[1]][1] != None:
            raise OccupiedSquareException("Square already occupied.")
        else:
            self.board[position[0]][position[1]][1] = tile