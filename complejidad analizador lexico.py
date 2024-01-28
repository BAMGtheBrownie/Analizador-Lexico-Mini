import re

def analizador_lexico(codigo):
    tokens = []
    reservadas = {'if': 19, 'while': 20, 'return': 21, 'else': 22, 'int': 4, 'float': 4, 'void': 4}
    patron_identificador = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')
    patron_entero = re.compile(r'\d+')
    patron_real = re.compile(r'\d+\.\d+')
    patron_operador = re.compile(r'[+\-*/=!<>]|&&|\|\|')
    patron_parentesis = re.compile(r'[()]')
    patron_llave = re.compile(r'[{}]')
    patron_punto_y_coma = re.compile(r';')
    patron_coma = re.compile(r',')
    patron_igual = re.compile(r'=')

    i = 0
    while i < len(codigo):
        if codigo[i].isspace():
            i += 1
        elif codigo[i].isalpha():
            match = patron_identificador.match(codigo, i)
            if match:
                lexema = match.group(0)
                tipo = reservadas.get(lexema, 0)
                tokens.append(('identificador', tipo))
                i = match.end()
            else:
                print(f"Error léxico: Caracter inesperado '{codigo[i]}' en la posición {i}")
                return None
        elif codigo[i].isdigit():
            match_entero = patron_entero.match(codigo, i)
            match_real = patron_real.match(codigo, i)
            if match_real and '.' in match_real.group(0):
                tokens.append(('real', 2))
                i = match_real.end()
            elif match_entero:
                tokens.append(('entero', 1))
                i = match_entero.end()
            else:
                print(f"Error léxico: Caracter inesperado '{codigo[i]}' en la posición {i}")
                return None
        else:
            match = None
            for patron, tipo in [(patron_operador, 'operador'), (patron_parentesis, 'parentesis'), 
                                 (patron_llave, 'llave'), (patron_punto_y_coma, 'punto_y_coma'),
                                 (patron_coma, 'coma'), (patron_igual, 'igual')]:
                match = patron.match(codigo, i)
                if match:
                    tokens.append((tipo, match.group(0)))
                    i = match.end()
                    break
            if not match:
                print(f"Error léxico: Caracter inesperado '{codigo[i]}' en la posición {i}")
                return None

    tokens.append(('fin', 23))
    return tokens

# Ejemplo de uso
codigo_fuente = """
int main() {
    int a = 10;
    float b = 3.14;
    if (a > 5 && b < 4.0) {
        return a + b;
    } else {
        return a * b;
    }
}
"""

tokens_resultantes = analizador_lexico(codigo_fuente)

if tokens_resultantes:
    print("Símbolo\t\tTipo")
    for token, tipo in tokens_resultantes:
        print(f"{token}\t\t{tipo}")
