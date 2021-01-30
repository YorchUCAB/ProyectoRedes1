from Classes.Player import Player
from Classes.Player import Player
from Classes.Card import Card
from Classes.Deck import Deck
import pygame,sys
import msvcrt

# Rutinas graficas:
#  Estas rutinas se correrán en el while principal
#  para que vayan actualizando las cartas de los jugadores

def showOthers():
    sep = 60
    for x in range(1,len(players)):
        if len(players[x].hand) <= 5:
            sep = 70    
        if len(players[x].hand) > 5 and len(players[x].hand) < 15 :
            sep = 40
        if len(players[x].hand) >= 15 :
            sep = 20     
        if x == 1:
            carta = pygame.image.load('img/card_back.png').convert() 
            carta = pygame.transform.rotate(carta,90)
        if x == 2: 
            carta = pygame.image.load('img/card_back.png').convert()
            carta = pygame.transform.rotate(carta,180)
        if x == 3: 
            carta = pygame.image.load('img/card_back.png').convert()
            carta = pygame.transform.rotate(carta,270)     
        for y in range(len(players[x].hand)):
            if x == 1: 
                Cx = 1050
                Cy = 100+y*sep
            if x == 2: 
                Cx = 300+y*sep
                Cy = -10
            if x == 3: 
                Cx = -45
                Cy = 100+y*sep
            screen.blit(carta,(Cx,Cy)) 

def showHand():
    for x in range(len(player1.hand)):
        screen.blit(player1.hand[x].surface,(player1.hand[x].x,player1.hand[x].y))          

def showDiscard():
    carta = identificar(discards[-1])
    screen.blit(carta,(600,250)) 

def showDeck():
    carta = pygame.image.load('img/card_back.png').convert()
    screen.blit(carta,(400,250)) 

#Rutinas logicas de dibujo
#Estas rutinas nos ayudan a asignarle a cada carta su imagen y posicion segun debe ser
#posteriormente fueron integradas a la clase player pero se mantienen aquí por si acaso se necesitaran
def identificar(cartaId):
    Mvalues = {
        1:"_1",
        2:"_2",
        3:"_3",
        4:"_4",
        5:"_5",
        6:"_6",
        7:"_7",
        8:"_8",
        9:"_9",
        "Doble manotazo":"_doble",
        "Reversa":"_reverse", 
        "Salta":"_skip",
        "Cambia color":"_wild", 
        "Ataque":"_ataque",
        "Tira un color":"_tiracolor",
        "Cuadruple manotazo":"_cuadruple"
    }
    Mcolours = {
        "Azul":"blue",
        "Rojo":"red",
        "Amarillo":"yellow",
        "Verde":"Green",
        "Comodin":"comodin"
    }
    # if cartaId.colour == "Comodin":
    #     carta = pygame.image.load('img/small/wild_color_changer.png').convert()
    #     return carta
    # if cartaId.value == "Tira un color":
    #     carta = pygame.image.load('img/small/card_back_alt.png').convert()
    #     return carta    
    valor = Mvalues.get(cartaId.value,"_back")
    color = Mcolours.get(cartaId.colour,"card")
    carta = pygame.image.load('img/{}{}.png'.format(color,valor)).convert()
    return carta

def asignHand():
    y=0
    if len(player1.hand) < 8:
        for x in range(len(player1.hand)):
            player1.hand[x].x = 180+x*110
            player1.hand[x].y = 520
    else:
        for x in range(int(len(player1.hand)/2)):
            player1.hand[x].x = 220+x*110
            player1.hand[x].y = 470
        for x in range(int(len(player1.hand)/2),len(player1.hand)):
            player1.hand[x].x = 200+y*110
            player1.hand[x].y = 600 
            y=y+1

#Especificamos los detalles de la pantalla
pygame.init()
screen = pygame.display.set_mode((1200,720))
pygame.display.set_caption("UNO Attack")
clock = pygame.time.Clock()

#Creamos el fondo
bg_surface = pygame.Surface([1200,720])
bg_surface.fill((46,57,102)) #Este es el color de fondo

#EMPIEZA EL JUEGO -------------------------------------------------------------------------------------

#Se crean los jugadores
player1 = Player()
player2 = Player()
player3 = Player()
player4 = Player()

#Se crea el mazo y se barajea
Deck = Deck()
Deck.shuffleDeck()

discards = [] #pila donde se van jugando las cartas

#Se reparten las cartas. Cada quien agarra 7 del Deck
player1.draw(7,Deck)
player2.draw(7,Deck)
player3.draw(7,Deck)
player4.draw(7,Deck)

players = [player1, player2, player3,player4]

Direction = 1 #1 para sentido horario. -1 para sentido antihorario

playerTurn = 0 #Turno de jugador

numPlayers = len(players)

discards.append(Deck.cards.pop(0)) #Agarramos la primera carta del mazo para ser la primera sobre la cual jugar

#Chequeamos que no se arranque con un comodin o con un Doble Manotazo
while discards[-1].colour == 'Comodin' or discards[-1].value == 'Doble manotazo':
    discards.append(Deck.cards.pop(0))

#Rescatamos la lista de colores
colourList = Deck.colours
#Y le quitamos el 4, que es Comodin
colourList.pop(4)

#Inicializamos el color
currentColour = discards[-1].colour #Variable para gestionar los cambios de color

#Variable para llevar la cantidad de Doble Manotazos que se han jugado en cadena
DobleManotazoTimes= 0
 
playing = True #Variable que indica si el juego sigue activo
asignHand()#asignamos a cada carta su posicion en pantalla


while playing:
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 
    #Verificamos que el mazo tenga mas de 10 cartas, para que no se quede vacio
    if len(Deck.cards) <= 30:
        for i in range(len(discards)-1):
            Deck.cards.append(discards.pop(0))  

    print ("")
    print ("-------------")
    print ("")
    print("jugador {}".format(playerTurn+1))
    print ("")
        
    #mostramos la carta del tope
    print("Carta en el tope de la pila: {} {}".format(discards[-1].colour, discards[-1].value))
    if (discards[-1].colour == "Comodin"):
        print('El color actual es {}'.format(currentColour))
    showDiscard()
    #Vemos si puede jugar
    if players[playerTurn].canPlay(discards[-1],Deck,currentColour,DobleManotazoTimes):
        #le mostramos su mano
        players[playerTurn].showHand()
        #Se inicializa la carta que se va a jugar
        numCardChosen = -1
        #Este while es para chequear que no seleccione algo invalido
        while numCardChosen == -1:
            if playerTurn == 0:
                print("Elige una carta para jugar")
                numNotChosen = True
                while numNotChosen:
                    pos = pygame.mouse.get_pos()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            for x in range(len(player1.hand)):
                                if player1.hand[x].isOver(pos):
                                    numCardChosen = x
                                    print('escogiste la carta {} de tu mano'.format(x))
                                    numNotChosen = False
                        if event.type == pygame.MOUSEMOTION:
                            for x in range(len(player1.hand)):
                                if player1.hand[x].isOver(pos):
                                    player1.asignHand() 
                                    player1.hand[x].y -= 20
                    #El juego necesita actualizar los graficos en cada ciclo para poder funcionar
                    screen.blit(bg_surface,(0,0))
                    showHand()
                    showOthers()  
                    showDiscard()
                    showDeck()
                    pygame.display.update()
                    clock.tick(120)
                #Esta linea es complicada.
                #Se elige del arreglo de jugadores el que tenga el turno
                #Luego se elige de la mano (arreglo hand) la carta [numCardChosen-1] y se rescata su color y valor        
                if (players[playerTurn].hand[numCardChosen].colour == "Comodin"
                    or players[playerTurn].hand[numCardChosen].colour == currentColour 
                    or players[playerTurn].hand[numCardChosen].value == discards[-1].value):

                    print("{} {}".format(players[playerTurn].hand[numCardChosen].colour, 
                                    players[playerTurn].hand[numCardChosen].value))
                    discards.append(players[playerTurn].hand.pop(numCardChosen))
                    currentColour = discards[-1].colour
                    players[playerTurn].asignHand #Rutina gráfica para reordenar las cartas del jugador
                    screen.blit(bg_surface,(0,0))
                    showHand()
                    showOthers()  
                    showDiscard()
                    showDeck()
                    pygame.display.update()
                    clock.tick(120)     
                else:
                    print("No puedes jugar esa carta")
                    numCardChosen = -1 #0 otra vez, para que el ciclo se repita
            else:
                print("Elige una carta para jugar")
                try:
                    numCardChosen = int(input())
                    #El numero que elija debe estar en su mazo
                    if not (1 <= numCardChosen <= len(players[playerTurn].hand)):
                        #Se salio del rango de su mazo
                        raise Exception
                
                    #Esta linea es complicada.
                    #Se elige del arreglo de jugadores el que tenga el turno
                    #Luego se elige de la mano (arreglo hand) la carta [numCardChosen-1] y se rescata su color y valor        
                    if (players[playerTurn].hand[numCardChosen-1].colour == "Comodin"
                        or players[playerTurn].hand[numCardChosen-1].colour == currentColour 
                        or players[playerTurn].hand[numCardChosen-1].value == discards[-1].value):

                        print("{} {}".format(players[playerTurn].hand[numCardChosen-1].colour, 
                                        players[playerTurn].hand[numCardChosen-1].value))
                        discards.append(players[playerTurn].hand.pop(numCardChosen-1))
                        currentColour = discards[-1].colour
                        players[playerTurn].asignHand #Rutina gráfica para reordenar las cartas del jugador
                        screen.blit(bg_surface,(0,0))
                        showHand()
                        showOthers()  
                        showDiscard()
                        showDeck()
                        pygame.display.update()
                        clock.tick(120)      
                    else:
                        print("No puedes jugar esa carta")
                        numCardChosen = -1 #0 otra vez, para que el ciclo se repita
                except ValueError: 
                    #Puso un caracter invalido
                    print("Entrada invalida")
                    print("")
                except Exception:
                    #Se salio de su mazo
                    print('Numero invalido')
                    numCardChosen = -1       
        print("")
        #Ahora que se jugó la carta, hay que ver que era para aplicar sus efectos
        #vamos con los comodines
        if discards[-1].colour == "Comodin":
            if discards[-1].value == "Ataque":
                print('')
                #Imprimos los jugadores
                for i in range(len(players)):
                    if (i != playerTurn):
                        print('{}) Jugador {}'.format(i+1, i+1))
                #Variable inicializada para el while
                print("")
                playerChosen = -1
                #Verificamos la eleccion
                while playerChosen == -1:
                    try:
                        playerChosen= int(input('Elije un jugador para atacar: '))-1
                        if not 0 <= playerChosen <= len(players)-1:
                            raise Exception
                        if playerChosen == playerTurn:
                            raise Exception
                    except ValueError:
                        print("Entrada invalida")
                        print("")
                        playerChosen = -1
                    except Exception:
                        if playerChosen == playerTurn:
                            print('¡ESE ERES TU!')
                        else:
                            print("Numero invalido")
                        print("")
                        playerChosen = -1
                #atacamos
                times = 0
                for times in range(2):
                    players[playerChosen].hand.extend(Deck.spitOutCards())
                    players[playerTurn].asignHand #Rutina gráfica para reordenar las cartas del jugador
                print("Atacaste al jugador {}".format(playerChosen+1))
                print("")
            elif discards[-1].value== "Cuadruple manotazo":
                times = 0
                #Si esta en el ultimo jugador, le toca agarrar al primero (+direction)
                if playerTurn == len(players)-1 and Direction == 1:
                    for times in range(4):                   
                        players[0].hand.extend(Deck.spitOutCards())
                #Si esta en el primero, le toca agarrar al ultimo (-direction)
                elif playerTurn == 0 and Direction == -1:
                    for times in range(4):                   
                        players[len(players-1)].hand.extend(Deck.spitOutCards())
                        players[playerTurn].asignHand #Rutina gráfica para reordenar las cartas del jugador
                else:
                    for times in range (4):
                        players[playerTurn+Direction].hand.extend(Deck.spitOutCards())
                        players[playerTurn].asignHand #Rutina gráfica para reordenar las cartas del jugador                

            #variable aux
            i = 0
            #Mostramos los colores
            for colour in colourList:
                i += 1
                print("{}) {}".format(i,colour))
            #Variable inicializada para el while
            print("")
            #Validamos su eleccion
            colourChosen = -1
            while colourChosen == -1:
                try:
                    colourChosen= int(input('Elije un color: '))-1
                    if not 0 <= colourChosen <= 3:
                        raise Exception
                except ValueError:
                    print("Entrada invalida")
                    print("")
                    colourChosen = -1
                except Exception:
                    print("Numero invalido")
                    print("")
                    colourChosen = -1
            #Cambiamos el color
            currentColour = colourList[colourChosen]
            print('Elegiste el color {}'.format(Deck.colours[colourChosen]))

        #Vamos con las demas
        elif discards[-1].value == "Doble manotazo":
            DobleManotazoTimes += 1
        elif discards[-1].value == "Reversa":
            Direction *= -1
            currentColour = discards[-1].colour
        elif discards[-1].value == "Salta":
            if playerTurn == len(players)-1 and Direction == 1:
                playerTurn = 0
            elif playerTurn == 0 and Direction == -1:
                playerTurn = len(players)-1
            else:
                playerTurn += Direction
            currentColour = discards[-1].colour
            print("Salta") #este print() es solo para que el programa pueda compilar mientras
        elif discards[-1].value == "Tira un color":

            #Variable aux
            i= 0
            #Contador de cartas bajadas
            discardsCount= 0
            for card in players[playerTurn].hand:
                if card.colour == currentColour:
                    discards.append(players[playerTurn].hand.pop(i))
                    discardsCount += 1
                else:
                    i+=1  
            print('')
            print('Bajaste {} cartas de color {}'.format(discardsCount, currentColour)) 
            print('') 
            currentColour = discards[-1].colour
        else: 
            #Es una carta normal
            print("Es normal")

    else:
        #Si no pudo jugar porque agarró 2, entonces hay que borrar la cadena de doble manotazo
        if (discards[-1].value == 'Doble manotazo'):
            DobleManotazoTimes = 0
        print("No puedes jugar. Tienes que pisar el boton de la maquina")
        print("Presione una tecla para continuar...")
        msvcrt.getch()
        print("*lo pisa*")
       
        players[playerTurn].hand.extend(Deck.spitOutCards())
        players[playerTurn].asignHand #Rutina gráfica para reordenar las cartas del jugador
    
    if len(players[playerTurn].hand) == 0:
        playing = False
    else:
        playerTurn += Direction
        if (playerTurn == len(players)):
            playerTurn = 0
        elif playerTurn < 0:
            playerTurn = len(players)-1                    
    screen.blit(bg_surface,(0,0))
    showHand()
    showOthers()  
    showDiscard()
    showDeck()
    pygame.display.update()
    clock.tick(120)

print('EL GANADOR ES EL JUGADOR {}'.format(playerTurn))