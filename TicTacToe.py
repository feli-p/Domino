"""
Este proyecto es un juego de gato (tic tac toe).
Está hecho para practicar programación en Python, por lo que contiene elementos innecesarios para el juego
pero que se usaron para practicar programación con clases en este lenguaje.
"""

import random

class Tablero:
    def __init__(self):
        self.dim = 3
        self.jugadas = [0]*9
        
    def imprimeTablero(self):
        tabla = """
        +---+---+---+
        | {} | {} | {} |
        +---+---+---+
        | {} | {} | {} |
        +---+---+---+
        | {} | {} | {} |
        +---+---+---+
        """
        print(tabla.format(*self.jugadas).replace('0','-').replace('-1', 'O').replace('1', 'X'))


class Jugador:
    def __init__(self):
        self.nombre = ""
        self.id = 0

    def setID(self, newID):
        self.id = newID

    def printID(self):
        print(self.id)


class JugadorHumano(Jugador):
    def __init__(self):
        super().__init__()
    
    def movimiento(self, tablero):
        bandera = True
        while(bandera):

            bandera2 = True
            while(bandera2):
                entradaUsuario = input("\tEscoge dónde poner tu figura:\t")
                if entradaUsuario.isdigit():
                    index = int(entradaUsuario)
                    if index > 8:
                        print("\t\tIngresa un número entre 0 y 8\n")
                    else:
                        bandera2 = False
                else:
                    print("\t\tIngresa un número entre 0 y 8\n")

            if tablero.jugadas[index] == 0:
                tablero.jugadas[index] = self.id
                bandera = False
            else:
                print("\t\tNúmero inválido, escoge de nuevo.\n")
            

class CPU(Jugador):
    def movimiento(self, tablero):
        bandera = True
        while(bandera):
            index = random.randint(0,8)
            if tablero.jugadas[index] == 0:
                tablero.jugadas[index] = self.id;
                bandera = False
    
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
        jugador1.setID(1)

        name2 = input("\tJugador 2:\n\t\t")
        if name2 != 'CPU':
            jugador2 = JugadorHumano()
            jugador2.nombre = name2
        else:
            jugador2 = CPU()
            jugador2.nombre = 'CPU 2'
        jugador2.setID(-1)

        self.jugadores.append(jugador1)
        self.jugadores.append(jugador2)
        print("\n")
    
    def jugada(self):
        print(f"Ronda {self.ronda+1}: ",end = '')
        aux = self.ronda % 2
        #turno = self.jugadores[aux].id
        print(f"Turno de {self.jugadores[aux].nombre}")
        
        self.jugadores[aux].movimiento(self.tablero)
        
        self.tablero.imprimeTablero()
        self.ronda += 1

    def revisarVictoria(self):
        resultado = 0
        if self.ronda+1 >= 2*self.tablero.dim-1:
            # Revisar Diagonales
            sum = 0
            for j in range(self.tablero.dim):
                sum += self.tablero.jugadas[(self.tablero.dim+1)*j]
            resultado = self.checksum(sum)

            if not(self.fin):
                sum = 0
                for j in range(self.tablero.dim):
                    sum += self.tablero.jugadas[(self.tablero.dim-1)*(j+1)]
                resultado = self.checksum(sum)

            # Revisar renglones
            i = 0
            while(not(self.fin) and i < self.tablero.dim):
                sum = 0
                for j in range(self.tablero.dim):
                    sum += self.tablero.jugadas[self.tablero.dim*i+j]
                resultado = self.checksum(sum)
                i += 1

            # Revisar columnas
            i = 0
            while(not(self.fin) and i < self.tablero.dim):
                sum = 0
                for j in range(self.tablero.dim):
                    sum += self.tablero.jugadas[i+self.tablero.dim*j]
                resultado = self.checksum(sum)
                i += 1
            
        return resultado

    def checksum(self, sum):
        resultado = 0
        if abs(sum) == self.tablero.dim:
            self.fin = True
            resultado = sum
        return resultado
            
    def iniciaPartida(self):
        self.crearJugadores()
        ganador = 0
        while(not(self.fin) and self.ronda < 9):
            self.jugada()
            ganador = self.revisarVictoria()
        if ganador == 0:
            print("¡Ha sido un empate!")
        else:
            i = 1
            if ganador == self.tablero.dim:
                i = 0
            print(f"Felicidades, {self.jugadores[i].nombre}. ¡Ganaste!")
            
        print("¡Gracias por jugar!")
        
        
if __name__=='__main__':
    print("""
            Bienvenidos al juego de gato
            Hecho por: losa lucines gpt
        ------------------------------------
          """)

    juego = Partida()
    juego.iniciaPartida()
    