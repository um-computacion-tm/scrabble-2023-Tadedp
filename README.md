# Scrabble

## Play the famous Scrabble on your terminal

**Scrabble** is a word game in which two to four players compete in forming words with lettered tiles on a board.

This project was designed to be played in **Spanish** language.

## Running Scrabble

To play Scrabble on Linux you must have Git and Docker installed on your device. 
Follow these steps:

 - Open your terminal and go to the directory where you want to save the game files.

 - Clone the repository using: 

```
    git clone https://github.com/um-computacion-tm/scrabble-2023-Tadedp.git
```

 - Inside the game directory, run the following command to create a docker image using the project's Dockerfile (you can also run it in a virtual environment):

```
    docker build -t [image name] .
```

 - Run the docker image using:

```
    docker run -it [image name]
```

 - Enjoy playing Scrabble!

## Rules

The players score points by placing tiles bearing a letter onto a 15x15 square game board. The tiles must form words that read left-to-right or top-to-bottom. As words are placed on the game board, points are gained. The objective when playing is to score more points than other players.

 - **Game Board**

The board consists of a 15x15 square grid of cells, also known as squares, each of which accommodates a single letter tile.

 - **Tiles**

There is a bag with 100 tiles that are used in the game and 98 of them will contain a letter and a point value ranging from 1 to 10, depending on how rare the letter usage is in standard Spanish and how difficult it may be to lay that letter playing a word. 

There are two blank tiles that are unmarked, have no point value and can be used as wild tiles to replace any letter. When played, a blank tile will remain as the letter it replaced and it will be marked on the board with an asterisk.

Point values for each letter:

**0 Points**: Blank tiles

**1 Point**: A, E, O, I, U, S, N, R, L, T

**2 Points**: D, G

**3 Points**: B, C, M, P

**4 Points**: F, H, V, Y

**5 Points**: Ch, Q

**8 Points**: J, Ll, Ñ, Rr, X

**10 Points**: Z

 - **Bonus Squares**

Some squares offer multipliers of two possible types: letter and word multipliers.

**Double and triple Letter Scores**: When the Lx2 or Lx3 cells on the board are used, they will double or triple the point value of the tile placed on that bonus square.

**Double and triple Word Score**: When the Wx2 or Wx3 cells on the board are used, the entire value of the word played will be doubled or tripled.

The bonus cells can only be used one time. After placing a tile in one of them, its multiplier cannot be used anymore by placing another word that uses the same square.

 - **Playing Scrabble**

Every player will start with seven tiles in their rack. There are three possible moves during any turn: play a word, exchange tiles for new tiles or pass.

When a player exchanges tiles, they can choose to exchange all the tiles they want that they currently hold in their rack, scoring nothing and ending their turn, and when a player passes, they will forfeit that turn.

 - **Placing a Word**

The first player will play their word so that they use the center star square. The star square will offer a double word score to the first word. 

All players following will play their words by using one or more tiles in their rack to place a word on the board. The main word **must** either use the letters of one or more previously played words or else have at least one of its tiles horizontally or vertically adjacent to an already played word in order to be a valid move. If any words other than the main word are formed, they are also scored.

Any word that can be found by searching for it in the [RAE DLE website](https://dle.rae.es/) can be used in the game. 

After playing tiles on the board, players will draw new tiles to replace those. If there are not enough tiles in the bag to replenish their rack to seven tiles, the player takes all the remaining tiles. 

 - **End of the Game**

The game ends when either all tiles are gone from the bag and a single player has placed all of their tiles or every player makes two consecutive passes (two complete rounds of just passes).

When the game ends, each player will reduce their accumulated score by the sum of the values of the tiles remaining on their racks. If a player ended the game and has no remaining tiles, they will add the sum of the values of the remaining tiles of the rest of players to their accumulated score.

The player with the highest score after all final scores are calculated wins.

## CircleCI Badges

### - main branch:
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/um-computacion-tm/scrabble-2023-Tadedp/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/um-computacion-tm/scrabble-2023-Tadedp/tree/main)

### - develop branch:
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/um-computacion-tm/scrabble-2023-Tadedp/tree/develop.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/um-computacion-tm/scrabble-2023-Tadedp/tree/develop)

## CodeClimate Badges
[![Maintainability](https://api.codeclimate.com/v1/badges/e57200e2cb6077584b6f/maintainability)](https://codeclimate.com/github/um-computacion-tm/scrabble-2023-Tadedp/maintainability)

[![Test Coverage](https://api.codeclimate.com/v1/badges/e57200e2cb6077584b6f/test_coverage)](https://codeclimate.com/github/um-computacion-tm/scrabble-2023-Tadedp/test_coverage)

## Authors

 - Tadeo Drube Perez - _Project developer_ - [Tadedp](https://github.com/Tadedp)  