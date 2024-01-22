import re

def analizador_lexico(codigo):
    tokens = []
    patron_identificador = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')
    patron_real = re.compile(r'\d+\.\d+')
    patron_simbolo_igual = re.compile(r'=')

    i = 0
    while i < len(codigo):
        if codigo[i].isspace():
            i += 1
        elif codigo[i].isalpha():
            match = patron_identificador.match(codigo, i)
            if match:
                tokens.append(('IDENTIFICADOR', match.group(0)))
                i = match.end()
            else:
                print(f"Error léxico: Caracter inesperado '{codigo[i]}' en la posición {i}")
                return None
        elif codigo[i].isdigit():
            match = patron_real.match(codigo, i)
            if match:
                tokens.append(('REAL', match.group(0)))
                i = match.end()
            else:
                print(f"Error léxico: Caracter inesperado '{codigo[i]}' en la posición {i}")
                return None
        elif codigo[i] == '=':
            tokens.append(('IGUAL', '='))
            i += 1
        else:
            print(f"Error léxico: Caracter inesperado '{codigo[i]}' en la posición {i}")
            return None

    return tokens

# Ejemplo de uso
codigo_fuente = "variable1 = 123.45"
tokens_resultantes = analizador_lexico(codigo_fuente)

if tokens_resultantes:
    print("Tokens:")
    for token in tokens_resultantes:
        print(token)
