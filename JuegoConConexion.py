from Classes.Player import Player
from Classes.Player import Player
from Classes.Card import Card
from Classes.Deck import Deck
from Classes.Buttons import Button
import pygame,sys
import msvcrt
from msvcrt import getch
import sys
import serial
import io
import random 
import time
import threading
import keyboard

# variables inicio globales
ver_valores = 1     # flag para imprimir valores para debug
alfa_num = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
mng_puerto_entrada = 0  #manejador del puerto de entrada
mng_puerto_salida =  0  #manejador del puerto de salida
str_id_PC = '' # string con el id de la PC
num_jugadores = 0 # numero de jugadores conectados (0-x) serian x+1 jugadores
str_PC_maestro = '' # string del serial de la PC maestro
seriales_jugadores = [] # list de seriales de todas las PC conectadas
#
# variables fin


# RUTINAS GRAFICAS:
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
    screen.blit(botonUno.surface,(botonUno.x,botonUno.y)) 

def showLabel():
    labelSurface = game_font.render(labelText,True,(255,255,255))
    labelRect = labelSurface.get_rect(center =(550,450))
    screen.blit(labelSurface,labelRect)

def showColorButtons():
    for x in range(len(botonesC)):
        screen.blit(botonesC[x].surface,(botonesC[x].x,botonesC[x].y))

def showPlayerButtons():
    for x in range(len(botonesJ)):
        if (x != playerTurn):
            screen.blit(botonesJ[x].surface,(botonesJ[x].x,botonesJ[x].y))

def showFlechas():
    screen.blit(flecha1,(900,150))
    screen.blit(flecha2,(150,400))   
    
#creamos los 4 botones para seleccionar un color
def createColorButtons():
    botonRojo = pygame.image.load('img/boton_rojo_sombra1.png')
    x = 180
    y = 300
    boton = Button(botonRojo,x,y)
    botonesC.append(boton)
    botonRojo = pygame.image.load('img/boton_verde_sombra1.png')
    x +=200
    y = 300 
    boton = Button(botonRojo,x,y)
    botonesC.append(boton)
    botonRojo = pygame.image.load('img/boton_azul_sombra1.png')
    x +=200
    y = 300 
    boton = Button(botonRojo,x,y)
    botonesC.append(boton)
    botonRojo = pygame.image.load('img/boton_amarillo_sombra1.png')
    x +=200
    y = 300
    boton = Button(botonRojo,x,y) 
    botonesC.append(boton)

#Creamos 3 botones para seleccionar el jugador
def createPlayerButtons():
    botonsurface =  button_font.render('J1',True,(255,255,255))
    x = 250
    y = 150
    boton = Button(botonsurface,x,y)
    botonesJ.append(boton)
    botonsurface =  button_font.render('J2',True,(255,255,255))
    x += 200
    y = 150
    boton = Button(botonsurface,x,y)
    botonesJ.append(boton) 
    botonsurface =  button_font.render('J3',True,(255,255,255))
    x += 200
    y = 150
    boton = Button(botonsurface,x,y)
    botonesJ.append(boton)
    botonsurface =  button_font.render('J4',True,(255,255,255))
    x += 200
    y = 150
    boton = Button(botonsurface,x,y)
    botonesJ.append(boton)    
#RUTINAS LOGICAS DE DIBUJO
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
game_font = pygame.font.Font('OpenSans-Bold.ttf',30)
button_font = pygame.font.Font('OpenSans-Bold.ttf',50)

#Creamos el fondo
bg_surface = pygame.Surface([1200,720])
bg_surface.fill((46,57,102)) #Este es el color de fondo

#Creamos las flechas de direccion
flecha1 = pygame.image.load('img/flecha3.png')
flecha1 = pygame.transform.rotozoom(flecha1,-90,0.1)
flecha2 = pygame.image.load('img/flecha3.png')
flecha2 = pygame.transform.rotozoom(flecha2,90,0.1)

#Creamos el boton UNO
carta = pygame.image.load('img/UNO_button.png') 
carta = pygame.transform.scale(carta,(150,150))
botonUno = Button(carta,380,250)

#Variables del juego
labelText = 'Que empiece el juego' #variable para el texto en pantalla
botonesC = [] #arreglo para guardar los botones de selccion de color
createColorButtons() #llenamos el arreglo de arriba
botonesJ = [] #arreglo para guardar los botones de seleccion de jugador
createPlayerButtons()

#RUTINAS DE CONEXIÓN----------------------------------------------------------------------------------

# Funciones

def buscar_Puertos_Seriales(): 
    # Funcion buscar_Puertos_Seriales Busca los poertos seriales fisicos en la PC (No necesariamente estan disponibles)
    # Parametros: sin parametros
    # Retorna: list ser_puertos [enteros con los puertos disponibles, string xx de puertos disponibles, manejadores sin inicializar del puerto]
    ports = ['COM%s' % (i + 1) for i in range(100)]
    puertos_com = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            puertos_com.append(port)
        except (OSError, serial.SerialException):
            pass
    # puertos_com=sorted(x[0] for x in comports()) # funcion de serial que retorna las compuertas seriales existentes en la PC
    #if ver_valores: print (puertos_com)
    est_puerto = []    # estructura del puerto serial individual
                        # contiene puerto X, COMX, 0 = int, string, manejador de puerto
    ser_puertos = []    # estructura con todos los puertos seriales disponibles est_puertos
    int_puertos_fisicos = len(puertos_com) # cantidad de puertos fisicos
    for p in range(0, int_puertos_fisicos):
        if(len(puertos_com[p])==5):   # si es un puerto COM >9 (tiene 5 caracteres) y asumiendo que no hay puertos COM >99
            int_dec=int(puertos_com[p][3])  # 1er caracter decena
            int_uni=int(puertos_com[p][4])  # 2nd caracter unidad
        else:
            int_dec=0                       # 1er caracter decena
            int_uni=int(puertos_com[p][3])  # 2nd caracter unidad
        str_puerto = "COM"+str(int_dec*10+int_uni) # cadena con el nombre del puerto
        try:    # intenta abrir el puerto esperando error o exito
            # abre el puerto para ver si esta disponible
            ser = serial.Serial(str_puerto, 9600, 8, timeout=1)
            ser.close() # se pudo abrir, se cierra el puerto
            est_puerto.append(int_dec*10+int_uni)      # agrega al vector de enteros el valor de com detectado X
            est_puerto.append(str_puerto)              # agrega al vector de string el valor de com detectado COMX
            est_puerto.append(0)                       # agrega manejador del puerto en 0
            #if ver_valores:print(str(int_dec*10+int_uni)+ " " + puertos_com[p])
            ser_puertos.append(est_puerto)            # agrega la informacion del puerto a la lista de puertos
        except serial.SerialException: # no se pudo abrir el puerto
            # if ver_valores:print(str_puerto+ " No disponible")
            pass
        est_puerto = [] # vacia el vector
    return ser_puertos # retorna la lista de puertos disponibles

def seleccionar_Puerto(puertos, accion):
    # Funcion seleccionar_Puerto
    # Parametros: list puertos,  string accion
    #             lista con los puertos disponibles, string con la accion a mostrar
    # Retorna: int_puertos puerto seleccionado (1 ...99) 0 para no seleccion
    sel=0 # bandera para el while
    int_puertos_disponibles = len(puertos) # cantidad de puertos disponibles
    while(sel==0):
        print("Escoja un puerto para " + accion)
        print(" 0 para cancelar")
        for p in range(0, int_puertos_disponibles):
            if(p>9):
                espacio=""
            else:
                espacio=" "
            print(espacio+str(int(p+1))+ " COM"+str(puertos[p][0]))
        puerto_sel=input("Su eleccion: ")
        try:
            puerto_sel=int(puerto_sel)
            if(puerto_sel==0):
                return 0
            if(puerto_sel <= int_puertos_disponibles):
                    sel=1    
                    continue
            else:
                print("Eleccion invalida " + str(puerto_sel))
                continue
        except ValueError:
            print("Eleccion invalida " + str(puerto_sel))
            continue
    # while end
    return puerto_sel
    
def configurar_Puertos_PC(lst_puertos_fisicos):
    # Funcion configurar_Puertos_PC
    # Parametros: lst_puertos_fisicos = listado de puertos fisicos
    # Retorna: list configPuertosPC [ent 1, sal 1] [ent 2, sal 2]
    lst_puertos=[]
    lst_puertos.append(seleccionar_Puerto(lst_puertos_fisicos, "entrada")-1) # entero del puerto de entrada X
    lst_puertos.append(seleccionar_Puerto(lst_puertos_fisicos, "salida")-1)  # entero del puerto de salida Y
    return lst_puertos

def serial_Write(str_data):
    # Funcion serial_Write
    # Parametros: data a esribir
    # Retorna: int data numero de bytes escritos
    # time.sleep(2)
    data = mng_puerto_salida.write(bytes(str_data.encode()))
    return data

def serial_Write_con_Respuesta(str_data):
    # Funcion serial_Write_Respuesta
    # Parametros: data a esribir
    # Retorna: serial de PC destino, nensaje a enviar, data completa leida formato decode
    # time.sleep(2)
    data = mng_puerto_salida.write(bytes(str_data.encode()))
    str_data_entrada = ''
    while(str_data_entrada==''):
        str_serial, str_mensaje, str_data_entrada = serial_Readline()
    return str_serial, str_mensaje, str_data_entrada  

def serial_Read(bytes_a_leer):
    # Funcion serial_Read
    # Parametros: bytes_a_leer (numero de bytes a leer)
    # Retorna: data leida formato decode
    data = mng_puerto_entrada.read(bytes_a_leer).decode()
    return data

def serial_Readline(): 
    # Funcion serial_Readline
    # Parametros:
    # Retorna: serial de PC destino, nensaje a enviar, data completa leida formato decode
    data = mng_puerto_entrada.readline().decode() 
    serial = data[0:10]
    mensaje = data[10:len(data)-1]
    return serial, mensaje, data

def busqueda_equipos_conectados(): 
    # busqueda_equipos_conectados
    # Parametros: 
    # Retorna: numeros de equipos conectados y seriales de equipos
    num_PC = 0
    listo=False
    str_serial = [] # crea lista de PC (Esta 1, la 2 es la anterior en el anilli y asi
    str_serial.append(str_id_PC) # agrega en la primera posicion la id de esta PC
    num_datos_escritos = serial_Write(str_id_PC) # envia este id ala PC siguiente
    # print("Enviando: "+ str_id_PC)
    # p = len(str_id_PC)
    
    print("Esperando conexion de otros equipos")
    while(not listo): # bucle para concatenar todas las PC del anillo
        str_data_entrada = ''
        while(str_data_entrada == ''): # espera por un id nuevo que se envie de la PC anterior
            str_data_entrada = serial_Read(10)
        # print("Recibiendo: "+ str_data_entrada)
        if (str_data_entrada == str_id_PC): # listo, dio la vuelta el serial de esta PC
                listo = True
        else:
            num_PC += 1
            str_serial.append(str_data_entrada) # agrega en la primera posicion la id de esta PC
            num_datos_escritos = serial_Write(str_data_entrada)
        #    print("Enviando: "+ str_data_entrada)
    # fin while        
    
    # voltea el vector de seriales para mas facil manejo
    # PC(actual), PC(Siguiente, que recibe de Maestro), ...PC Ultimo(Su siguiente es el Maestro)
    id_sentido_salida = [str_serial[0]]
    for p in range(num_PC,0,-1):
        id_sentido_salida.append(str_serial[p])
    return(num_PC, id_sentido_salida)

def iniciar_partida(solicitar_inicio_partida, name):
    # iniciar_partida (usa hilo)
    # Parametros: solicitar_inicio_partida [], name = nombre del thread
    # Retorna: nada
    print("Presione ("+solicitar_inicio_partida[0]+") para ser Maestro e iniciar partida\n")
    print("Si va a ser Esclavo solo espere")
    tecla = solicitar_inicio_partida[0]
    seguir_hilo = True
    while(seguir_hilo):
        if keyboard.is_pressed(tecla) == True:
            getch()
            seguir_hilo = False
            solicitar_inicio_partida[1] = 's'
        elif solicitar_inicio_partida[1] == 's':
            seguir_hilo = False
    return

def iniciar_partida_manual(): 
    # Inicia partida manual. 
    # Parametros: 
    # Retorna: id de la PC maestra
    solicitar_inicio_partida = []
    solicitar_inicio_partida.append(str_id_PC[0])
    solicitar_inicio_partida.append('')
        
    hilo_solicitar = threading.Thread(target = iniciar_partida, args =(solicitar_inicio_partida, 'thread_inicio'))
    print("Esperando que alguien inicie partida")
    hilo_solicitar.start()
        
    str_data_entrada=''
    
    # num_datos_escritos = serial_Write(mng_puerto_salida, str_data_salida)
    while(str_data_entrada==''):
        str_data_entrada = serial_Read(10)
        if(solicitar_inicio_partida[1]=='s'): #esta PC solicito un inicio de partida
            print("Esta PC solicito inicio de partida")
            str_data_entrada=str_id_PC
    solicitar_inicio_partida[1] = 's' # para que el hilo termine
    # manda info de master a la siguiente PC
    num_datos_escritos = serial_Write(str_data_entrada)
        
    # si esta es la PC que solicito ser master, va a recibir la cadena que envio de regreso por el anillo
    if str_data_entrada==str_id_PC:    # espera a que el mensaje llegue
        str_data_entrada=''  
        while(str_data_entrada==''):
            str_data_entrada = serial_Read(10)
        
    return (str_data_entrada)

def liberar_Esclavas():
    # liberar_Esclavas
    # Parametros: 
    # Retorna: nada
    for p in range(num_jugadores, -1,-1):
        num_datos_escritos = serial_Write(seriales_jugadores[p]+'\n')
        # no espera respuesta porque el anillo se rompe
        print(f"{seriales_jugadores[p]} PC {p} Termino")

    return
# Inicio de programa

# ser = serial.Serial("COM1", 9600, 8, timeout=1) para ocupar cualquier com 

# genera ID de la PC de 10 caracteres a partir de la variable alfa_num, declarada al comienzo,
# podemos considerarla unica ya que la probabilidad que se repita en 2, 3 ....o N ocasiones es muy baja
str_id_PC = ""
for p in range(0,10):
    str_id_PC = str_id_PC + str(alfa_num[random.randint(0, len(alfa_num)-1)]) 

# identifica los puertos seriales de la PC, devuelve lista con [X, "COMX", manejador del puerto=0], desecha los que estan abiertos
lst_puertos_fisicos = buscar_Puertos_Seriales() # solo son los puertos disponibles para usar

# str_nombre_PC = input("Nombre de la PC: ")
str_nombre_PC = "Perico de los Palotes"

# lst_puertos_PC = lista de [COM entrada, COM salida] de la PC
lst_puertos_PC = configurar_Puertos_PC(lst_puertos_fisicos)

# estos mng_puerto_xxxx solo tienen el manejador de puerto del COM de entrada, salida de la PC
mng_puerto_entrada = serial.Serial(lst_puertos_fisicos[lst_puertos_PC[0]][1], 9600, 8, timeout=1)
if(lst_puertos_PC[0] ==lst_puertos_PC[1]):
    mng_puerto_salida = mng_puerto_entrada  # si es el mismo puerto de entrada y salida
else:    
    mng_puerto_salida = serial.Serial(lst_puertos_fisicos[lst_puertos_PC[1]][1], 9600, 8, timeout=1)

print(f"Recibiendo por: " + mng_puerto_entrada.name + " Enviando por: "+ mng_puerto_salida.name)

# busca conexiones hasta recibir respuesta, cerrandose el anillo serial
print("Asegurese de que todas la PCs estan encendidas y\ndebidamente conectados sus cables seriales.")
print("Yo puedo conectarlas, pero no puedo hacer magia.")
print("El numero de jugadores a conectarse es ilimitado (Minimo 2).")
print("Presione una tecla para buscar jugadores")
getch()

num_jugadores, seriales_jugadores = busqueda_equipos_conectados() #str_id_PC, mng_puerto_entrada, mng_puerto_salida)
print(f"Numero de jugadores encontrados: {num_jugadores+1}")
print(f"Serial de esta PC: {str_id_PC}")
print("Seriales de PCs Conectadas:")
print(seriales_jugadores)

# espera por inicio de partida por alguno de los jugadores
# busca quien empezara la partida para personalizarla,
# por lo tanto sera el maestro y las demas esclavas
str_PC_maestro = iniciar_partida_manual()

# establece flag maestro = 1 o 0 para esta PC
print("PC Maestro: " + str_PC_maestro)
if(str_PC_maestro==str_id_PC): # esta es la PC maestro
    print("Esta PC es Maestro.")
    maestro=1
else:                        # esta PC es esclavo
    maestro=0
    print("Esta PC es Esclava.")
    
print(seriales_jugadores)



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
    labelText = 'Es el turno del jugador {}'.format(playerTurn+1)
    print ("")
        
    #mostramos la carta del tope
    print("Carta en el tope de la pila: {} {}".format(discards[-1].colour, discards[-1].value))
    #enviamos la carta al jugador siguiente
    

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
                        if event.type == pygame.MOUSEBUTTONDOWN: #Detectamos el click
                            for x in range(len(player1.hand)):
                                if player1.hand[x].isOver(pos):
                                    numCardChosen = x
                                    print('escogiste la carta {} de tu mano'.format(x))
                                    numNotChosen = False
                        if event.type == pygame.MOUSEMOTION: #Efecto hover de carta
                            for x in range(len(player1.hand)):
                                if player1.hand[x].isOver(pos):
                                    player1.asignHand() 
                                    player1.hand[x].y -= 20
                    #El juego necesita actualizar los graficos en cada ciclo para poder funcionar
                    screen.blit(bg_surface,(0,0))
                    showFlechas()
                    showHand()
                    showOthers()  
                    showDiscard()
                    showDeck()
                    showLabel()
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
                    showFlechas()
                    showOthers()  
                    showDiscard()
                    showDeck()
                    showLabel()
                    pygame.display.update()
                    clock.tick(120)     
                else:
                    print("No puedes jugar esa carta")
                    numCardChosen = -1 #0 otra vez, para que el ciclo se repita
            else:
                players[playerTurn].asignHand #Rutina gráfica para reordenar las cartas del jugador
                screen.blit(bg_surface,(0,0))
                showHand()
                showFlechas()
                showOthers()  
                showDiscard()
                showDeck()
                showLabel()
                pygame.display.update()
                clock.tick(120) 
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
                        showFlechas()
                        showOthers()  
                        showDiscard()
                        showDeck()
                        showLabel()
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
                    if playerTurn == 0:
                        labelText = 'Elije un jugador para atacar:'
                        playerNotChosen = True
                        while playerNotChosen:
                            pos = pygame.mouse.get_pos()
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    for x in range(len(botonesJ)):
                                        if botonesJ[x].isOver(pos):
                                            playerChosen = x
                                            playerNotChosen = False
                                if event.type == pygame.MOUSEMOTION:
                                    for x in range(len(botonesJ)):
                                        if botonesJ[x].isOver(pos):
                                            botonesJ[x].setSurfaceJ2(x,button_font)
                                        else:
                                            botonesJ[x].setSurfaceJ1(x,button_font)    
                            #El juego necesita actualizar los graficos en cada ciclo para poder funcionar
                            screen.blit(bg_surface,(0,0))
                            showHand()
                            showFlechas()
                            showOthers()  
                            showDiscard()
                            showDeck()
                            showLabel()
                            showPlayerButtons()
                            pygame.display.update()
                            clock.tick(120)
                    else:    
                        try:
                            playerChosen = int(input('Elije un jugador para atacar: '))-1
                            labelText = 'Elije un jugador para atacar:'
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
                if playerTurn == 0:
                    colorNotChosen = True
                    while colorNotChosen:
                        pos = pygame.mouse.get_pos()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                for x in range(len(botonesC)):
                                    if botonesC[x].isOver(pos):
                                        colourChosen= x
                                        colorNotChosen = False
                            if event.type == pygame.MOUSEMOTION:
                                for x in range(len(botonesC)):
                                    if botonesC[x].isOver(pos):
                                        botonesC[x].setSurface2(x)
                                    else:
                                        botonesC[x].setSurface1(x)    
                        #El juego necesita actualizar los graficos en cada ciclo para poder funcionar
                        screen.blit(bg_surface,(0,0))
                        showHand()
                        showFlechas()
                        showOthers()  
                        showDiscard()
                        showDeck()
                        showLabel()
                        showColorButtons()
                        pygame.display.update()
                        clock.tick(120)
                else:
                    try:
                        colourChosen= int(input('Elije un color: '))-1
                        labelText = 'Elije un color'
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
            labelText = 'Elegiste el color {}'.format(Deck.colours[colourChosen])

        #Vamos con las demas
        elif discards[-1].value == "Doble manotazo":
            DobleManotazoTimes += 1
        elif discards[-1].value == "Reversa":
            Direction *= -1
            currentColour = discards[-1].colour
            flecha1 = pygame.transform.flip(flecha1,False,True) #estas cuatro lineas las quise hacer en una funcion cambiarFlechas()
            flecha1 = pygame.transform.rotozoom(flecha1,90,1)# pero no se por que no funcionó, asi que lo puse aquí
            flecha2 = pygame.transform.flip(flecha2,False,True)
            flecha2 = pygame.transform.rotozoom(flecha2,90,1)
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
        if playerTurn == 0:
            #Si no pudo jugar porque agarró 2, entonces hay que borrar la cadena de doble manotazo
            if (discards[-1].value == 'Doble manotazo'):
                DobleManotazoTimes = 0 
            labelText = 'No puedes jugar ninguna carta, presiona el boton UNO'    
            buttonNotPressed = True
            while buttonNotPressed:
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN: #Detectamos el click
                        for x in range(len(player1.hand)):
                            if botonUno.isOver(pos):
                                players[playerTurn].hand.extend(Deck.spitOutCards())
                                buttonNotPressed = False
                    if event.type == pygame.MOUSEMOTION: #Efecto hover de carta
                        for x in range(len(player1.hand)):
                            if botonUno.isOver(pos):
                                botonUno.setBotonUno(2)
                            else:    
                                botonUno.setBotonUno(1)
                #El juego necesita actualizar los graficos en cada ciclo para poder funcionar
                screen.blit(bg_surface,(0,0))
                showHand()
                showFlechas()
                showOthers()  
                showDiscard()
                showDeck()
                showLabel()
                pygame.display.update()
                clock.tick(120)    
        else:    
            #Si no pudo jugar porque agarró 2, entonces hay que borrar la cadena de doble manotazo
            if (discards[-1].value == 'Doble manotazo'):
                DobleManotazoTimes = 0  
            print("No puedes jugar. Tienes que pisar el boton de la maquina")
            print("Presione una tecla para continuar...")
            msvcrt.getch()
            print("*lo pisa*")
            players[playerTurn].hand.extend(Deck.spitOutCards())
            showHand()
            showFlechas()
            showOthers()  
            showDiscard()
            showDeck()
            showLabel()
            pygame.display.update()
            clock.tick(120)
    
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
    showFlechas()
    showOthers()  
    showDiscard()
    showDeck()
    showLabel()
    pygame.display.update()
    clock.tick(120)

print('EL GANADOR ES EL JUGADOR {}'.format(playerTurn))