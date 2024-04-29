# analizador_sintactico.py

from Analizador_Lexico import TokenType, Token

class AnalizadorSintactico:
    def __init__(self):
        pass

    def analizar(self, tokens):
        self.tokens = tokens
        self.posicion = 0
        self.actual = None
        self.error = False
        self.ultimo_token = None

        self.avanzar()

        # Comenzar análisis sintáctico
        self.programa()

        if not self.error and self.ultimo_token.type == TokenType.FIN_ARCHIVO:
            print("Análisis sintáctico completado correctamente.")
        else:
            print("Error de sintaxis.")

    def avanzar(self):
        if self.posicion < len(self.tokens):
            self.actual = self.tokens[self.posicion]
            self.posicion += 1
        else:
            self.actual = Token(TokenType.FIN_ARCHIVO, '', 0)

    def coincidir(self, tipo_esperado):
        if self.actual.type == tipo_esperado:
            self.avanzar()
        else:
            self.error = True
            print(f"Error de sintaxis: Se esperaba '{tipo_esperado}', se encontró '{self.actual.type}' en la línea {self.actual.line}.")

    def programa(self):
        # Aquí iría la lógica para analizar la estructura general del programa
        pass
