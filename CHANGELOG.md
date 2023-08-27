# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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