# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2023-10-29

### Fixed

 - codeclimate configuration to test cognitive complexity as intended (threshold of 15).
 - an issue that caused blank tiles used as double letters (CH, LL and RR) not showing correctly in the board once they were played.
 - an issue that caused the bag to return the same tiles to the player instead of giving different ones in exchange moves.   
 
### Changed
 
 - Board class and its test locations to new files to improve maintainability. 
 - various methods to reduce their cognitive complexity by refactoring them without changing its functionality.  

## [1.0.0] - 2023-10-11

### ¡¡¡Scrabble is now playable!!! 

### Added

 - Main.
 - ScrabbleCli class: 
   - Methods: client() -> None, getPlayersCount() -> _int_ playersCount, getPlayerMove() -> _int_ move, getWordInputs() -> (_str_ word, _int_ increasingCoordinate, _(int)_ firstTilePosition), getExchangeInputs(_int_ bagLen, _Player_ player) -> _[int]_ positions, getKeepPlayingInputs() -> None, getFinalScores( _[Player]_ players) -> _[int]_ scores.
 - Exceptions:
   - WordIsNotInDictionary exception.
   - WordIsNotInsideBoard exception.
   - WordPlacementIsNotValid exception.
   - PlayerDoesNotHaveNeededTiles exception.
   - InsufficientTilesInBag exception.
 - Methods in ScrabbleGame Class: getBoard() -> _Board_ board, getPlayerRack() -> _Player_ currentPlayer, getBagRemainingTiles() -> _int_ tiles, getPlayers() -> _[Player]_ players, playWord(_str_ mainWord, _int_ increasingCoordinate, _(int)_ firstTilePosition) -> None, exchangeTiles( _[int]_ positions) -> None, validateMove( _[[str, Tile]]_ words, _int_ increasingCoordinate, _(int)_ firstTilePosition), playing(_int_ consecutivePasses) -> Bool, getPositions( _str_ cutMainWord) -> _[int]_ positions.
 - test.sh script to run codeclimate and coverage locally.

### Removed

 - All previous exceptions except DictionaryConnectionFailed exception.
 
## [0.20.0] - 2023-10-4

### Added

 - formedWords method in Board class: formedWords(_str_ word, _int_ increasingCoordinate, _(int)_ firstTilePosition) -> _[str]_ words 
 - searchExtraWord method in Board class: searchExtraWord(_int_ increasingCoordinate, _(int)_ letterPosition, _str_ letter) -> _str_ word 

### Fixed

 - validNotInitialMove() method in Board Class. The method was not considering the board limits. Now it only checks the sorrounding squares if their indeces is between 0 and 14. 

## [0.19.0] - 2023-10-1

### Added

 - DictionaryConnectionFailed exception.

### Changed

 - isInDictionary() method in Dictionary class to raise DictionaryConnectionFailed exception when pyrae.dle.search_by_word() fails.

### Fixed

 - validFirstMove() method in Board Class. The method was not considering the case of one letter words as invalid moves. Now the first word must also be at least two letters long to be considered valid. 
 - validNotInitialMove() method in Board Class. The method was not considering the case of adjacent words as valid moves. Now both cases (adjacent words and using already played tiles) are considered valid moves. 
 - Board class constructor. The square corresponding to the coordinates (7, 7) was not being counted as a premium square. Now it is also a double word score square.
 - Log level of dle module used in dictionary module to not show log messages while playing the game. 

## [0.18.0] - 2023-09-26

### Added

 - repr() method in Board class.

### Changed

 - repr() method in Square class so that it only returns the content of the square (bonus or tile), not its outline.

### Fixed
 
 - putBonuses() method in Board class. Squares accesed from board with the same bonuses and in symmetrical positions were the same objects, making that changing one of them changed all. Now they all work as different objects. 

## [0.17.0] - 2023-09-25

### Added

 - repr() method in Tile, Square and Player classes for their string representation during command line execution.

## [0.16.0] - 2023-09-24

### Added

 - Dictionary class:
   - Attributes: None
   - Methods: isInDictionary(_str_ word) -> Bool 

## [0.15.0] - 2023-09-23

### Added

 - haveTiles method in Player class: haveTiles(_str_ word) -> Bool 

## [0.14.0] - 2023-09-20

### Added

 - validNotInitialMove method in Board class: validNotInitialMove(_str_ word, _int_ increasingCoordinate, _(int)_ firstTilePosition) -> Bool 

## [0.13.0] - 2023-09-18

### Added

 - wordIsValid method in Board class(different method from the one added in version 0.12.0): wordIsValid(_str_ word, _int_ increasingCoordinate, _(int)_ firstTilePosition) -> Bool
 - validFirstMove method in Board class: validFirstMove(_str_ word, _int_ increasingCoordinate, _(int)_ firstTilePosition) -> Bool

### Changed 

 - definition of wordIsValid method added in version 0.12.0: wordIsInside(_str_ word, _int_ increasingCoordinate, _(int)_ firstTilePosition) -> Bool
 - definition of checkBoardTiles method added in version 0.9.0: checkBoardTiles(_(int)_ actualTilePosition, _[(int)]_ boardTiles) -> Bool

## [0.12.0] - 2023-09-12

### Added

 - wordIsValid method in Board class: wordIsValid(_int_ wordLen, _int_ increasingCoordinate, _(int)_ firstTilePosition) -> Bool
 - data type specification in all parameters of each method. 

## [0.11.0] - 2023-09-10

### Added

 - nextTurn method in ScrabbleGame class: nextTurn() -> None
   
## [0.10.0] - 2023-09-09

### Added

 - ScrabbleGame class:
   - Attributes: _Board_ board, _TileBag_ tileBag, _[Player]_ players, _int_ currentPlayer

## [0.9.0] - 2023-09-07

### Changed

 - putWord method in Board class, divided in three methods (putHorizontalWord, putVerticalWord and checkBoardTile) for an easier code maintainability.

## [0.8.0] - 2023-09-05

### Added

 - sumScore method in Player class: sumScore(_int score_) -> None

## [0.7.0] - 2023-09-04

### Added

 - Integration with CodeClimate.
 - README document to show CodeClimate and CircleCI badges.
 - putBonuses method in Board class: putBonuses(_[(int, int)]_ coordinates, _(int, str)_ bonus) -> None

### Changed
 
 - TileBag and Board constructors to a clearer and shorter ones.  

## [0.6.0] - 2023-08-29

### Added

 - Integration with CircleCI.
 - Requirements.txt to contain references to the packages used in the project.
 - resetBonus method in Square class: resetBonus() -> None

### Changed

 - wordScore now uses resetBonus after using the value of a premium square with a newly placed tile.

## [0.5.0] - 2023-08-27

### Changed

 - Board class put(_Tile_ tile, _(int, int)_ position) to putWord(_[Tile]_ newTiles, _int_ increasingCoordinate, _(_int_, _int_)_ firstTilePosition, _[Tile]_ boardTilesPositions) -> None, now adding an entire word instead of a single tile.
 - method of raising OccupiedSquare exception.

## [0.4.0] - 2023-08-26

### Added

 - tile attribute in Square class: _Tile_ tile
 - putTile method in Square class: putTile(_Tile_ tile) -> None
 - squareValue method in Square class: squareValue() -> _int_ value

### Changed

 - Board class attribute board type from _[[[Square, Tile]]]_ to _[[Square]]_, saving from now on the Tile objects used by players in Square class instead of Board class, for a clearer and more intuitive code.  

### Fixed

 - Board class attribute board usage in Board class methods due to the change in its definition.

## [0.3.0] - 2023-08-22

### Added

 - Player class:
    - Attributes: _[Tile]_ rack, _int_ score
    - Methods: takeTiles(_[Tile]_ tiles) -> None, giveTiles(_str_ letters) -> _[Tile]_ tiles
 - MissingTileInRack exception.
 - wordScore method in Board class: wordScore(_(int, int)_ firstTilePosition) -> _int_ score 

### Fixed

 - Missing exception in 0.2.0 'Added' section on this changelog.

## [0.2.0] - 2023-08-21

### Added
 
 - Square class:
    - Attributes: _int_ multiplier, _char_ bonusType
 - Board class:
    - Attributes: _[[[Square, Tile]]]_ board
    - Methods: put(_Tile_ tile, _(int, int)_ position) -> None
 - OccupiedSquare exception.

## [0.1.0] - 2023-08-20

### Added

 - This CHANGELOG to document the changes to the project Scrabble.
 - Tests folder to contain every unit test that verify that the individual units of the source code fulfill their expected functionality. 
 - Game folder to contain every file that make the game work.
 - Models file to contain the classes corresponding to the game elements(Tile, Player, Board, etc.).
 - Tile class:
    - Attributes: _char_ letter, _int_ value
 - TileBag class:
    - Attributes: _[Tile]_ tiles
    - Methods: take(_int_ count) -> _[Tile]_ tiles, put(_[Tile]_ tiles) -> None
 - EmptyBag exception.