from game.scrabbleGame import ScrabbleGame
from game.models import Player

class ScrabbleCli:    
    def client(self):
        print("")
        print("SCRABBLE".center(151, "="))
        playersCount = ScrabbleCli.getPlayersCount()
        scrabbleGame = ScrabbleGame(playersCount)
        turnStart = True
        currentPlayer = 1
        consecutivePasses = 0
        scrabbleGame.nextTurn()
        print("")
        print("¡Comienzo del juego!".center(151))

        while scrabbleGame.playing(consecutivePasses):
            if turnStart:
                print("")
                print("Turno del jugador " + str(currentPlayer) + ": ")
                print(scrabbleGame.getBoard())
                print(scrabbleGame.getPlayerRack())
                turnStart = False
                
            move = ScrabbleCli.getPlayerMove()
            if move == 1:
                word, increasingCoordinate, firsTilePosition = ScrabbleCli.getWordInputs()
                try:
                    scrabbleGame.playWord(word, increasingCoordinate, firsTilePosition)
                except Exception as e:
                    print(e)
                    print("")
                    continue    
                consecutivePasses = 0
            
            elif move == 2:
                positions = ScrabbleCli.getExchangeInputs(scrabbleGame.getBagRemainingTiles(), scrabbleGame.getPlayerRack())
                try:
                    scrabbleGame.exchangeTiles(positions)
                except Exception as e:
                    print(e)
                    print("")
                    continue
                consecutivePasses = 0
                
            elif move == 3:
                consecutivePasses += 1
                
            
            currentPlayer = ScrabbleCli.endOfTurn(scrabbleGame, currentPlayer, playersCount)    
            if currentPlayer == 0:        
                break
            
            scrabbleGame.nextTurn()
            turnStart = True   
        
        ScrabbleCli.endOfGame(scrabbleGame)
    
    def endOfTurn(scrabbleGame: ScrabbleGame, currentPlayer: int, playersCount: int):
        print(" ")
        print("Puntajes:")
        players = scrabbleGame.getPlayers()
        for i in range(len(players)):
            print(">> Jugador " + str(i + 1) + ": " + str(players[i].score) + " pts.")
            
        keepPlaying = ScrabbleCli.getKeepPlayingInputs()
        if keepPlaying:        
            if currentPlayer == playersCount:
                currentPlayer = 1
            else:    
                currentPlayer += 1         
            return currentPlayer
        
        else:        
            return 0
    
    def endOfGame(scrabbleGame: ScrabbleGame):
        print("")
        print("Resultados finales:")
        winner = [0]
        finalScores = []
        playerScores, playerDiscounts, discountSum = ScrabbleCli.getFinalScores(scrabbleGame.getPlayers())
        for i in range(len(playerScores)):
            if playerDiscounts[i] > 0:
                finalScore = playerScores[i] - playerDiscounts[i]
                print(">> Jugador " + str(i + 1) + " (-" + str(playerDiscounts[i]) + 
                      " puntos por fichas restantes): " + str(finalScore) + " pts.")
            else:
                finalScore = playerScores[i] + discountSum
                print(">> Jugador " + str(i + 1) + " (+" + str(discountSum) + 
                      " puntos por fichas restantes del resto): " + str(finalScore) + " pts.")

            finalScores.append(finalScore)
            if i > 0 and finalScore == finalScores[winner[0]]:
                winner.append(i)
            if finalScore > finalScores[winner[0]]:
                winner = [i] 
        
        print(" ")
        winnerScore = finalScores[winner[0]]
        if len(winner) > 1:
            print("Los ganadores, con " + str(winnerScore) + " puntos, son: ")
            for i in range(len(winner)):
                print(">> Jugador " + str(winner[i] + 1))
        else:
            print("¡El ganador es el jugador " + str(winner[0] + 1) + " con " + str(winnerScore) + " puntos!")
        print("¡Felicidades!")
    
    def getPlayersCount():
        while True:
            try: 
                playersCount = int(input("Ingrese cantidad de jugadores: "))
                if playersCount < 2 or playersCount > 4 or not (str(playersCount).isdigit()):
                    raise ValueError
                break
            except ValueError:
                print("Error. Ingrese un valor entre 2 y 4.")
        return playersCount
    
    def getPlayerMove():
        while True:
            try: 
                move = int(input("Seleccione: 1) Colocar palabra ó 2) Cambiar fichas ó 3) Pasar -> "))
                if move < 1 or move > 3: 
                    raise ValueError
                break
            except ValueError:
                print("Error. Ingrese un valor entre 1 y 3.")
        return move
    
    def getWordInputs():
        while True:
            try: 
                word = input(">> Ingrese la palabra: ")
                if not word.isalpha():
                    raise ValueError
                word = word.upper()
                
                orientation = input(">> Ingrese la orientación de la palabra (H/V): ")
                if not orientation.isalpha() or (orientation.upper() != "H" and orientation.upper() != "V"):
                    raise ValueError
                
                if orientation.upper() == "V":
                    increasingCoordinate = 0
                else:
                    increasingCoordinate = 1
                
                print("Ingrese las coordenadas de la primer letra: ")
                firstTileRow = int(input(">> Fila (1-15): ")) - 1
                firstTileColumn = int(input(">> Columna (1-15): ")) - 1
                firstTilePosition = (firstTileRow, firstTileColumn)
                break
            
            except ValueError:
                print("Error. Verifique los datos ingresados y vuelva a intentarlo.")
        return word, increasingCoordinate, firstTilePosition

    def getExchangeInputs(bagLen: int, player: Player):
        print("Ingrese las fichas que desea cambiar (1-7, \"0\" atril completo, \"T\" terminar cambio): ")
        positions = []
        playerRack = player.rack
        while True:
            try:
                exchangeInput = input(">> ")
                if exchangeInput == "T" or exchangeInput == "t":
                    break
                
                exchangeInput = int(exchangeInput)
                if exchangeInput == 0:
                    return [i for i in range(len(playerRack))]
                else:        
                    ScrabbleCli.appendPositions(exchangeInput, playerRack, positions)
                
                if len(positions) == bagLen or len(positions) == len(playerRack):
                    break
            
            except ValueError:
                print("Error. Verifique el dato ingresado y vuelva a intentarlo.")
                continue
        return positions
        
    def appendPositions(exchangeInput: int, playerRack: list, positions: list):
        if exchangeInput > 0 and exchangeInput < (len(playerRack) + 1) and not (exchangeInput - 1) in positions:
            positions.append(exchangeInput - 1)                
        else:
            raise ValueError

    def getKeepPlayingInputs():
        while True:
            keepPlaying = input("¿Continuar jugando? (S/N): ")
            try:
                
                if keepPlaying.upper() == "N":
                    return False
                elif keepPlaying.upper() == "S":
                    return True
                else:
                    raise ValueError
            
            except ValueError:
                print("Error. Ingrese \"S\" o \"N\".")
                continue
    
    def getFinalScores(players: list):
        scores = []
        discounts = []
        discountSum = 0
        for i in range(len(players)):
            playerScore = players[i].score
            discount = 0
            if len(players[i].rack) > 1:   
                for tile in players[i].rack:
                   discount += tile.value
            
            discountSum += discount        
            discounts.append(discount)
            scores.append(playerScore)
        
        return scores, discounts, discountSum                