from game.scrabbleGame import ScrabbleGame

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
                print("Turno del jugador " + str(currentPlayer) + ": ")
                print(scrabbleGame.getBoard())
                print(scrabbleGame.getPlayerRack())
                turnStart = False
                
            try:
                move = ScrabbleCli.getPlayerMove()
            except Exception as e:
                print(e)
                continue
            
            if move == 1:
                word, increasingCoordinate, firsTilePosition = ScrabbleCli.getWordInputs()
                try:
                    scrabbleGame.playWord(word, increasingCoordinate, firsTilePosition)
                except Exception as e:
                    print(e)
                    continue    
                consecutivePasses = 0
            
            elif move == 2:
                positions = ScrabbleCli.getExchangeInputs(scrabbleGame.getBagRemainingTiles(), scrabbleGame.getPlayerRack())
                try:
                    scrabbleGame.exchangeTiles(positions)
                except Exception as e:
                    print(e)
                    continue
                consecutivePasses = 0
                
            elif move == 3:
                consecutivePasses += 1
                
            
            print(" ")
            print("Puntajes:")
            players = scrabbleGame.getPlayers()
            for i in range(len(players)):
                print(">> Puntaje jugador " + str(i + 1) + ": " + str(players[i].score))
                
            keepPlaying = ScrabbleCli.getKeepPlayingInputs()
            if keepPlaying:        
                if currentPlayer == playersCount:
                    currentPlayer = 1
                else:    
                    currentPlayer += 1         
                    
                scrabbleGame.nextTurn()
                turnStart = True   
            
            else:        
                break
        
        print("")
        print("Resultados finales:")
        winner = 0
        finalScores = ScrabbleCli.getFinalScores(scrabbleGame.getPlayers())
        for i in range(len(finalScores)):
            if finalScores[i] > finalScores[winner]:
                winner = i
            print(">> Jugador " + str(i + 1) + ": " + str(finalScores[i]))
        
        print(" ")
        winnerScore = finalScores[winner]
        if finalScores.count(winnerScore) > 1:
            print("Los ganadores con " + str(winnerScore) + " puntos son: ")
            for i in range(len(finalScores)):
                if finalScores[i] == winnerScore:
                    print(">> Jugador " + str(i + 1))
        else:
            print("¡El ganador es el jugador " + str(winner + 1) + " con " + str(winnerScore) + " puntos!")
        print("¡Felicidades!")
        return
    
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
                move = int(input("Seleccione: 1) Colocar palabra ó 2) Robar fichas ó 3) Pasar -> "))
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
                firstTileRow = int(input(">> Fila: ")) - 1
                firstTileColumn = int(input(">> Columna: ")) - 1
                firstTilePosition = (firstTileRow, firstTileColumn)
                break
            
            except ValueError:
                print("Error. Verifique los datos ingresados y vuelva a intentarlo.")
        return word, increasingCoordinate, firstTilePosition

    def getExchangeInputs(bagLen: int, playerRack: list):
        print("Ingrese las fichas que desea cambiar (1 a 7, \"0\" para atril completo, \"T\" terminar): ")
        positions = []
        exchangeInput = -1
        while exchangeInput != "T" and exchangeInput != "t":
            try:
                exchangeInput = input(">> ")
                exchangeInput = int(exchangeInput)
                if exchangeInput == 0:
                    return [i for i in range(len(playerRack))]
                else:        
                    if exchangeInput > 0 and exchangeInput < (len(playerRack) + 1) and not (exchangeInput - 1) in positions:
                        positions.append(exchangeInput - 1)                
                    else:
                        raise ValueError

                if len(positions) == bagLen or len(positions) == len(playerRack):
                    break
            
            except ValueError:
                print("Error. Verifique el dato ingresado y vuelva a intentarlo.")
                continue
            
        print(positions)
        return positions
        
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
        emptyRackPlayer = None
        for i in range(len(players)):
            playerScore = players[i].score
            discount = 0
            if len(players[i].rack) > 1:   
                for tile in players[i].rack:
                   discount += tile.value
            else:
                emptyRackPlayer = i
                    
            playerScore = playerScore - discount
            discounts.append(discount)
            scores.append(playerScore)
        
        if emptyRackPlayer != None:
            for discount in discounts:
                scores[emptyRackPlayer] += discount
        
        return scores                