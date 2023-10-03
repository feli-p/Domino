"""
Losa lucines gpt.
Inteligencia Artificial. ITAM.

Proyecto 1: Dominó con minimax
"""

import random
from time import time
import numpy as np
import re


def tiempo_transcurrido(f):
    """
    Decorador.
    Ejecuta la función y calcula el tiempo transcurrido.
    """
    def wrapper():
        inicio = time()
        # Regresa el valor de la función original.
        fun = f()
        tiempo_total = time() - inicio
        print("Tiempo transcurrido: %0.4f segundos." % tiempo_total)
        return fun
    
    return wrapper


def creaFicha(txt):
    """
    Función para pedir fichas al usuario, verificar que sean válidas y darles el formato correcto.
    In:     txt - cadena de texto con la información de la ficha.
    Out:    res - None si no se puede crear la ficha o una ficha formateada como tupla.
    """
    res = None
    ficha = re.findall("\d",txt)
    if len(ficha) == 2:
        ficha = [int(x) for x in ficha]
        if 0 <= ficha[0] <= 6 and 0 <= ficha[1] <= 6:
            ficha.sort()
            res = tuple(ficha)
        else:
            print('Ficha inexistente.')
    else:
        print("Entrada inválida.")
    return res


class Tablero:
    """
    Generalización del tablero de Dominó.
    Almacena la información necesaria de la partida y verifica movimientos.
    Imprime una versión resumida de las fichas en juego.
    """
    def __init__(self):
        self.left = -1
        self.right = -1
        self.fichas = np.zeros((7,7))
        self.pozo = 14
        
        
    def imprimeTablero(self):
        """
        Imprime el tablero en la linea de comandos
        """
        tabla = """
                    +---+---+---+
                    | {} |...| {} |
                    +---+---+---+
                """

        print(tabla.format(self.left,self.right))


    def primerFicha(self, ficha, idJugador):
        """
        Hacer el primer movimiento.
        IN: ficha -> int[2]
            idJugador -> int 
        """
        if self.left==-1 and self.right==-1:
            self.left = ficha[0]
            self.right = ficha[1]
            self.fichas[ficha] = idJugador


    def colocarFicha(self, ficha, lado, idJugador):
        """
        Agregar una ficha al tablero
        IN: ficha -> int[2]
            lado -> char
            idJugador -> int
        """
        success = -1
        
        if self.fichas[ficha] == 0:
            if lado=='I':
                if ficha[0]==self.left:
                    self.left = ficha[1]
                    self.fichas[ficha] = idJugador
                    success = 1
                elif ficha[1]==self.left:
                    self.left = ficha[0]
                    self.fichas[ficha] = idJugador
                    success = 1
                else:
                    print('Movimiento invalido')
            else:
                if ficha[0]==self.right:
                    self.right = ficha[1]
                    self.fichas[ficha] = idJugador
                    success = 1
                elif ficha[1]==self.right:
                    self.right = ficha[0]
                    self.fichas[ficha] = idJugador
                    success = 1
                else:
                    print('Movimiento invalido')
        else:
            print('La ficha ya esta en el tablero.')
                    
        return success
                    

    def valoraTablero():
        """
        Evaluar cuando se acaba la partida. Victoria o otra cosa
        """
        pass


class Jugador:
    """
    Define la clase genérica de Jugador sobre la cual se crearán CPU y JugadorHumano.
    Esta clase contiene las funciones genéricas de los jugadores.
    """
    def __init__(self):
        self.nombre = ""
        self.id = 0
        self.fichas = []
        self.pasar = False #Si esta bandera esta prendida el jugador no tiene movimentos validos, por lo que debera pasar


    def numFichas(self):
        """
        Devuelve el número de fichas que tiene un jugador
        """
        return len(self.fichas)


class JugadorHumano(Jugador):
    """
    Esta clase permite que los usuarios jueguen contra la computadora.
    Maneja la 
    """
    def inicializarFichas(self):
        self.fichas = [1]*7


    def primerMovimiento(self, tablero):
        """
        Primer movimiento del jugador humano
        In: tablero -> Tablero
        """
        print(f'Jugador {self.nombre} ¿Qué ficha vas a tirar?')
        bandera = True
        while bandera:
            movi = input('→')
            movi = creaFicha(movi)
            if bool(movi): # Se cumple si movi es distinto None
                tablero.primerFicha(movi,self.id)
                self.fichas = self.fichas[:-1] #Quitamos una ficha
                bandera = False


    def movimiento(self, tablero):
        """
        Movimiento del Jugador Humano (por consola)
        In: tablero -> Tablero
        """
        print(f'Jugador {self.nombre} ¿Qué ficha vas a tirar? [0:Pasar|1:Comer]')
        bandera = True
        self.pasar = False
        while bandera:
            movi = input('→ ')
            if movi == '0':
                if tablero.pozo == 0:
                    self.pasar = True
                    bandera = False
                else:
                    print('Aún hay fichas en el pozo.')
            elif movi == '1':
                if tablero.pozo > 0:
                    self.fichas.append(1) #agregamos una ficha
                    tablero.pozo -= 1
                else:
                    print('El pozo está vacío.')
            else:
                movi = creaFicha(movi)
                if bool(movi):
                    print('¿De que lado? [I/D]')
                    lado = input('→ ')
                    if lado.upper() == 'D':
                        bandera = tablero.colocarFicha(movi, 'D', self.id) == -1
                        if not bandera:
                            self.fichas = self.fichas[:-1] #Quitamos una ficha
                    elif lado.upper() == 'I':
                        bandera = tablero.colocarFicha(movi, 'I', self.id) == -1
                        if not bandera:
                            self.fichas = self.fichas[:-1] #Quitamos una ficha
                    else:
                        print('Lado no válido. Ingresa la ficha de nuevo.')
        print(self.numFichas())


class CPU(Jugador):
    """
    Jugador de Dominó automatizado con Inteligencia Artificial.
    Utiliza un algoritmo minimax para buscar el mejor movimiento disponible de acuerdo a una heurística.
    """
    def __init__(self):
        super().__init__()


    def inicializarFichas(self):
        """
        Ingresar las fichas asignadas al CPU
        """
        print('\t\tIngresa las 7 fichas.')
        for i in range(7):
            bandera = False
            while not bandera:
                aux = input(f'Ingresa la ficha {i} →')
                aux = creaFicha(aux)
                if bool(aux):
                    bandera = self.darFicha(aux)


    def darFicha(self, ficha):
        """
        Validar que la ficha no esté repetida
        IN: ficha -> int [2]
        OUT: success -> bool
        """
        success = False
        if ficha not in self.fichas:
            self.fichas.append(ficha)
            success = True
        else:
            print("Ficha repetida")
        return success


    def minmax(self, node, depth, maxPlayer):
        """
        Algoritmo de búsqueda MINIMAX
        IN: node -> Node
            depth -> int
            maxPlayer -> bool
        """
        pass
    

    def heuristica(self):
        """
        Función heurística: evalúa un estado del juego y asigna un valor
        dependiendo del jugador al que más favorezca.
        """
        pass


    def primerMovimiento(self, tablero):
        """
        Primer movimiento del CPU
        In: tablero -> Tablero
        """
        print('No implementado')
    

    def movimiento(self, tablero):
        """
        Hacer un movimiento del CPU
        In: tablero -> Tablero
        """
        print('No implementado')


class Nodo():
    def __init__(self):
        self.turnoCPU = True
        self.fichasCPU = []
        self.fichasDesconocidas = []
        self.left = -1
        self.right = -1
        self.pozo = -1

        
    def iniciaHijo(self, ficha, isLeft, valor):
        hijo = Nodo()
        hijo.turnoCPU = not(self.turnoCPU)
        hijo.pozo = self.pozo
        hijo.fichasCPU = self.fichasCPU[::]
        hijo.fichasDesconocidas = self.fichasDesconocidas[::]
        
        if self.turnoCPU:    
            hijo.fichasCPU.remove(ficha)    
        else:
            hijo.fichasDesconocidas.remove(ficha)

        if isLeft:
            hijo.left = valor
            hijo.right = self.right
        else:
            hijo.right = valor
            hijo.left = self.left

        hijo.pozo = self.pozo

        return hijo
            
        
    def creaHijo(self, ficha):
        hijo = None
        
        if ficha[0]==self.left:
            hijo = self.iniciaHijo(ficha, True, ficha[0])
        elif ficha[0]==self.right:
            hijo = self.iniciaHijo(ficha, False, ficha[0])
        elif ficha[1]==self.left:
            hijo = self.iniciaHijo(ficha, True, ficha[1])
        elif ficha[1]==self.right:
            hijo = self.iniciaHijo(ficha, False, ficha[1])

        return hijo

        
    def expande(self):
        resp = []
        fichas = self.fichasCPU if self.turnoCPU else self.fichasDesconocidas
        
        for ficha in fichas:
            aux = self.creaHijo(ficha)
            if bool(aux):
                resp.append(aux)

        return resp


class Partida():
    def __init__(self):
        self.tablero = Tablero()
        self.ronda = 1
        self.fin = False
        self.jugadores = []


    def crearJugadores(self):
        """
        Dar de alta los nombres de los jugadores,
        si se elige CPU entonces juega la máquina
        """
        print("Introduce el nombre de los jugadores. Si escribes CPU, el jugador correspondiente será la computadora.")
        name1 = input("\tJugador 1:\n\t\t→ ")
        if name1 != 'CPU':
            jugador1 = JugadorHumano()
            jugador1.nombre = name1
        else:
            jugador1 = CPU()
            jugador1.nombre = 'CPU 1'
        jugador1.id = 1
        jugador1.inicializarFichas()

        name2 = input("\tJugador 2:\n\t\t→ ")
        if name2 != 'CPU':
            jugador2 = JugadorHumano()
            jugador2.nombre = name2
        else:
            jugador2 = CPU()
            jugador2.nombre = 'CPU 2'
        jugador2.id = -1
        jugador2.inicializarFichas()

        print('¿Qué jugador tira primero?')
        print('[1] {}'.format(jugador1.nombre))
        print('[2] {}'.format(jugador2.nombre))
        bandera = True
        while bandera:
            jugador = input("→ ")
            if jugador=="1":
                self.jugadores.append(jugador1)
                self.jugadores.append(jugador2)
                bandera = False
            elif jugador=="2":
                self.jugadores.append(jugador2)
                self.jugadores.append(jugador1)
                bandera = False
            else:
                print("Opción incorrecta.")
        print()  

    
    def jugada(self):
        """
        Movimiento de alguno de los jugadores
        """
        print(f"Ronda {self.ronda+1}: ")
        aux = self.ronda % 2

        self.jugadores[aux].movimiento(self.tablero)
        
        self.tablero.imprimeTablero()
        self.ronda += 1
        

    def revisarVictoria(self):
        """
        Revisar si alguien ya ganó la partida
        """
        if not (self.jugadores[0].pasar and self.jugadores[1].pasar): 
            if self.jugadores[0].numFichas()==0:
                print(f"El jugador {self.jugadores[0].nombre} ganó.")
                self.fin = True
            elif self.jugadores[1].numFichas()==0:
                print(f'El jugador {self.jugadores[0].nombre} ganó.')
                self.fin = True
        else:
            self.fin = True
            print('Empate.')
                
            
    def iniciaPartida(self):
        """
        Iniciar una partida
        """
        self.crearJugadores()
        self.jugadores[0].primerMovimiento(self.tablero)
        self.tablero.imprimeTablero()
                
        
if __name__=='__main__':
    print("""
            Bienvenidos al juego de domino
            Hecho por: losa lucines gpt
        ------------------------------------
          """)

    nodo = Nodo()
    nodo.fichasCPU = [(1,2),(6,6),(6,5),(1,4)]
    nodo.left = 4
    nodo.right = 6
    print(nodo.expande())

    """
    partida = Partida()
    partida.iniciaPartida()
    #print(partida.jugadores[0].fichas)
    #print(partida.jugadores[1].fichas)
    jugadaConTiempo = tiempo_transcurrido(partida.jugada)
    while not(partida.fin):
        jugadaConTiempo()
        #partida.jugada()
        partida.revisarVictoria()
    
    """
