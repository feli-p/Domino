"""
Losa lucines gpt.
Inteligencia Artificial. ITAM.

Proyecto 1: Dominó con minmax
"""

import random
import numpy as np

class Tablero:
    def __init__(self):
        self.left = -1
        self.right = -1
        self.fichas = np.zeros(7)
        
    def imprimeTablero(self):
        tabla = """
                    +---+---+---+
                    | {} |...| {} |
                    +---+---+---+
                """

        print(tabla.format(self.left,self.right))

    def valoraTablero():
        """
        Evaluar cuando se acaba la partida. Victoria o otra cosa
        """
        pass


class Jugador:
    def __init__(self):
        self.nombre = ""
        self.id = 0
        self.fichas = []

    def numFichas(self):
        return len(self.fichas)
    

class CPU(Jugador):
    def __init__(self):
        super().__init__()

    def inicializarFichas(self):
        for i in range(7):
            bandera = True
            while bandera:
                aux = input("Ingresa ficha: \t").split(",")
                aux = [int(x) for x in aux]
                aux.sort()
                aux = tuple(aux)
                # Usar un try-except
                bandera = self.darFicha(aux) == -1


    def darFicha(self, ficha):
        success = -1
        if type(ficha) is tuple and len(ficha) == 2:
            if 0 <= ficha[0] <= 6 and 0 <= ficha[1] <= 6:
                if ficha not in self.fichas:
                    self.fichas.append(ficha)
                    success = 1
                else:
                    print("Ficha repetida")
            else:
                print("Ficha inexistente")
        else:
            print("Formato inválido")
        return success
    
    def movimiento(self, tablero):
        pass
            

class JugadorHumano(Jugador):
    def inicializarFichas(self):
        self.fichas = [1]*7

    def movimiento(self, tablero):
        pass
    
    def minmax(self):
        # test
        pass

    def heuristica(self):
        pass


class Partida():
    def __init__(self):
        self.tablero = Tablero()
        self.ronda = 0
        self.fin = False
        self.jugadores = []

    def crearJugadores(self):
        print("Introduce el nombre de los jugadores. Si escribes CPU, el jugador correspondiente será la computadora.")
        name1 = input("\tJugador 1:\n\t\t")
        if name1 != 'CPU':
            jugador1 = JugadorHumano()
            jugador1.nombre = name1
        else:
            jugador1 = CPU()
            jugador1.nombre = 'CPU 1'
        jugador1.id = 1
        jugador1.inicializarFichas()

        name2 = input("\tJugador 2:\n\t\t")
        if name2 != 'CPU':
            jugador2 = JugadorHumano()
            jugador2.nombre = name2
        else:
            jugador2 = CPU()
            jugador2.nombre = 'CPU 2'
        jugador2.id = -1
        jugador2.inicializarFichas()

        self.jugadores.append(jugador1)
        self.jugadores.append(jugador2)
        print("\n")
    
    def jugada(self):
        pass

    def revisarVictoria(self):
        pass

    def checksum(self, sum):
        pass
            
    def iniciaPartida(self):
        self.crearJugadores()
        
        
if __name__=='__main__':
    print("""
            Bienvenidos al juego de domino
            Hecho por: losa lucines gpt
        ------------------------------------
          """)
    partida = Partida()
    partida.iniciaPartida()
    print(partida.jugadores[0].fichas)
    print(partida.jugadores[1].fichas)
    