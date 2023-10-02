"""
Losa lucines gpt.
Inteligencia Artificial. ITAM.

Proyecto 1: Dominó con minimax
"""

import random
import numpy as np

class Tablero:
    def __init__(self):
        self.left = -1
        self.right = -1
        self.fichas = np.zeros((7,7))
        self.pozo = 14
       

    def imprimeTablero(self):
        tabla = """
                    +---+---+---+
                    | {} |...| {} |
                    +---+---+---+
                """

        print(tabla.format(self.left,self.right))


    def primerFicha(self, ficha, idJugador):
        if self.left==-1 and self.right==-1:
            self.left = ficha[0]
            self.right = ficha[1]
            self.fichas[ficha] = idJugador


    def colocarFicha(self, ficha, lado, idJugador):
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
    def __init__(self):
        self.nombre = ""
        self.id = 0
        self.fichas = []
        self.pasar = False #Si esta bandera esta prendida el jugador no tiene movimentos validos, por lo que debera pasar


    def numFichas(self):
        return len(self.fichas)


    def validaFicha(self, ficha):
        success = False
        if type(ficha) is tuple and len(ficha) == 2:
            if 0 <= ficha[0] <= 6 and 0 <= ficha[1] <= 6:
                if ficha not in self.fichas:
                    success = True
                else:
                    print("Ficha repetida")
            else:
                print("Ficha inexistente")
        else:
            print("Formato inválido")
        return success


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
        if self.validaFicha(ficha):
            self.fichas.append(ficha)
            success = 1
        return success


    def minmax(self, node, depth, maxPlayer):
        pass
    

    def heuristica(self):
        pass


    def primerMovimiento(self, tablero):
        print('No implementado')
    

    def movimiento(self, tablero):
        print('No implementado')
            

class JugadorHumano(Jugador):
    def inicializarFichas(self):
        self.fichas = [1]*7


    def primerMovimiento(self, tablero):
        print(f'Jugador {self.nombre} ¿Qué ficha vas a tirar?')
        bandera = True
        while bandera:
            # usar try - except
            movi = input('-> ')
            movi = movi.split(',')
            movi = [int(x) for x in movi]
            movi.sort()
            movi = tuple(movi)
            if self.validaFicha(movi):
                tablero.primerFicha(movi,self.id)
                self.fichas = self.fichas[:-1] #Quitamos una ficha
                bandera = False

                
    def movimiento(self, tablero):
        print(f'Jugador {self.nombre} ¿Qué ficha vas a tirar? [0:Pasar|1:Comer]')
        bandera = True
        self.pasar = False
        while bandera:
            movi = input('-> ')
            if movi == '0':
                self.pasar = True
                bandera = False
            elif movi == '1':
                if tablero.pozo > 0:
                    self.fichas.append(1) #agregamos una ficha
                    tablero.pozo -= 1
                else:
                    print('El pozo está vacío.')
            else:
                movi = movi.split(',')
                movi = [int(x) for x in movi]
                movi.sort()
                movi = tuple(movi)
                if self.validaFicha(movi):
                    print('¿De que lado? [I/D]')
                    lado = input('-> ')
                    if lado.upper() == 'D':
                        bandera = tablero.colocarFicha(movi, 'D', self.id) == -1
                        if not bandera:
                            self.fichas = self.fichas[:-1] #Quitamos una ficha
                    elif lado.upper() == 'I':
                        bandera = tablero.colocarFicha(movi, 'I', self.id) == -1
                        if not bandera:
                            self.fichas = self.fichas[:-1] #Quitamos una ficha
                    else:
                        print('Movimiento no valido. Ingresa la ficha de nuevo.')
        print(self.numFichas())


class Partida():
    def __init__(self):
        self.tablero = Tablero()
        self.ronda = 1
        self.fin = False
        self.jugadores = []


    def crearJugadores(self):
        print("Introduce el nombre de los jugadores. Si escribes CPU, el jugador correspondiente será la computadora.")
        name1 = input("\tJugador 1:\n\t\t-> ")
        if name1 != 'CPU':
            jugador1 = JugadorHumano()
            jugador1.nombre = name1
        else:
            jugador1 = CPU()
            jugador1.nombre = 'CPU 1'
        jugador1.id = 1
        jugador1.inicializarFichas()

        name2 = input("\tJugador 2:\n\t\t-> ")
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
            jugador = input("-> ")
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
        print(f"Ronda {self.ronda+1}: ")
        aux = self.ronda % 2

        self.jugadores[aux].movimiento(self.tablero)
        
        self.tablero.imprimeTablero()
        self.ronda += 1
        

    def revisarVictoria(self):
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
        self.crearJugadores()
        self.jugadores[0].primerMovimiento(self.tablero)
        self.tablero.imprimeTablero()
                
        
if __name__=='__main__':
    print("""
            Bienvenidos al juego de domino
            Hecho por: losa lucines gpt
        ------------------------------------
          """)
    
    partida = Partida()
    partida.iniciaPartida()
    #print(partida.jugadores[0].fichas)
    #print(partida.jugadores[1].fichas)
    while not(partida.fin):
        partida.jugada()
        partida.revisarVictoria()
    
    
