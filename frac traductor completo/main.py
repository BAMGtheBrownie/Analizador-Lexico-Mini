# main.py

from Analizador_Lexico import AnalizadorLexico
from Analizador_Sintactico import AnalizadorSintactico
from Traductor import Traductor
from lexer import TokenType, Token
from Harbol import Harbol


def main():
    # Aquí puedes solicitar la entrada del usuario, cargar el código fuente, etc.
    codigo_fuente = input("Ingresa el código fuente: ")

    # Crear el analizador léxico
    lexico = AnalizadorLexico(codigo_fuente)
    tokens = lexico.analizar()

    # Crear el analizador sintáctico
    sintactico = AnalizadorSintactico(tokens)
    arbol_sintactico = sintactico.analizar()

    # Crear el traductor y traducir el árbol sintáctico
    traductor = Traductor(arbol_sintactico)
    traduccion = traductor.traducir()

    # Imprimir la traducción
    print("Traducción:")
    print(traduccion)

if __name__ == "__main__":
    main()
