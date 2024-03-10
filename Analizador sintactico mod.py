import re

class ElementoPila:
    pass

class Terminal(ElementoPila):
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

class NoTerminal(ElementoPila):
    def __init__(self, nombre):
        self.nombre = nombre

class Estado(ElementoPila):
    def __init__(self, nombre):
        self.nombre = nombre

class Alumno:
    def __init__(self, codigo):
        self.codigo = codigo

    def muestra(self):
        pass

class Bachillerato(Alumno):
    def __init__(self, codigo, preparatoria):
        super().__init__(codigo)
        self.preparatoria = preparatoria

    def muestra(self):
        print("Alumno Bachillerato")
        print("Codigo:", self.codigo)
        print("Preparatoria:", self.preparatoria, end="\n\n")

class Licenciatura(Alumno):
    def __init__(self, codigo, carrera, creditos):
        super().__init__(codigo)
        self.carrera = carrera
        self.creditos = creditos

    def muestra(self):
        print("Alumno Licenciatura")
        print("Codigo:", self.codigo)
        print("Carrera:", self.carrera)
        print("Creditos:", self.creditos, end="\n\n")

class Pila:
    def __init__(self):
        self.lista = []

    def push(self, x):
        self.lista.insert(0, x)

    def pop(self):
        x = self.lista[0]
        del self.lista[0]
        return x

    def top(self):
        return self.lista[0]

    def muestra(self):
        print("Pila:", end=" ")
        for x in reversed(self.lista):
            x.muestra()
        print()

# Analizador Sintáctico
class AnalizadorSintactico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def analizar(self):
        try:
            self.sentencia()
            print("Análisis sintáctico exitoso.")
        except Exception as e:
            print(f"Error sintáctico: {e}")

    def sentencia(self):
        if self.tokens[self.posicion][0] == 'tipo':
            self.declaracion()
        else:
            self.expresion()

    def declaracion(self):
        self.tipo()
        self.identificador()
        self.match(('igual', '='))
        self.valor()

    def tipo(self):
        tipos_permitidos = {'int', 'float'}
        if self.tokens[self.posicion][1] in tipos_permitidos:
            self.match(('tipo', None))
        else:
            raise Exception(f"Error sintáctico: Se esperaba un tipo, pero se encontró {self.tokens[self.posicion][1]}")

    def identificador(self):
        self.match(('identificador', None))

    def valor(self):
        if self.tokens[self.posicion][0] == 'entero' or self.tokens[self.posicion][0] == 'real':
            self.match((self.tokens[self.posicion][0], None))
        else:
            raise Exception(f"Error sintáctico: Se esperaba un valor, pero se encontró {self.tokens[self.posicion][1]}")

    def expresion(self):
        self.termino()
        while self.posicion < len(self.tokens) and self.tokens[self.posicion][1] in ('+', '-'):
            self.match(('operador', '+') if self.tokens[self.posicion][1] == '+' else ('operador', '-'))
            self.termino()

    def termino(self):
        self.factor()
        while self.posicion < len(self.tokens) and self.tokens[self.posicion][1] in ('*', '/'):
            self.match(('operador', '*') if self.tokens[self.posicion][1] == '*' else ('operador', '/'))
            self.factor()

    def factor(self):
        if self.tokens[self.posicion][0] == 'entero' or self.tokens[self.posicion][0] == 'real':
            self.match((self.tokens[self.posicion][0], None))
        elif self.tokens[self.posicion][1] == '(':
            self.match(('parentesis', '('))
            self.expresion()
            self.match(('parentesis', ')'))
        else:
            raise Exception(f"Error sintáctico: Factor inesperado {self.tokens[self.posicion][1]}")

    def match(self, esperado):
        if self.posicion < len(self.tokens) and self.tokens[self.posicion] == esperado:
            self.posicion += 1
        else:
            raise Exception(f"Se esperaba {esperado}, pero se encontró {self.tokens[self.posicion]}")

# Analizador Léxico
class AnalizadorLexico:
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.tokens = []
        self.reservadas = {'if': 19, 'while': 20, 'return': 21, 'else': 22, 'int': 4, 'float': 4, 'void': 4}
        self.patron_identificador = re.compile(r'[a-zA-Z][a-zA-Z0-9]*')
        self.patron_entero = re.compile(r'\d+')
        self.patron_real = re.compile(r'\d+\.\d+')
        self.patron_operador = re.compile(r'[+\-*/=!<>]|&&|\|\|')
        self.patron_parentesis = re.compile(r'[()]')
        self.patron_llave = re.compile(r'[{}]')
        self.patron_punto_y_coma = re.compile(r';')
        self.patron_coma = re.compile(r',')
        self.patron_igual = re.compile(r'=')
        self.posicion = 0

    def analizar(self):
        while self.posicion < len(self.codigo_fuente):
            self.tokenizar()

    def tokenizar(self):
        if self.codigo_fuente[self.posicion].isspace():
            self.posicion += 1
        elif self.codigo_fuente[self.posicion].isalpha():
            match = self.patron_identificador.match(self.codigo_fuente, self.posicion)
            if match:
                lexema = match.group(0)
                tipo = self.reservadas.get(lexema, 0)
                self.tokens.append((NoTerminal(lexema), tipo))
                self.posicion = match.end()
            else:
                raise Exception(f"Error léxico: Caracter inesperado '{self.codigo_fuente[self.posicion]}' en la posición {self.posicion}")
        elif self.codigo_fuente[self.posicion].isdigit():
            match_entero = self.patron_entero.match(self.codigo_fuente, self.posicion)
            match_real = self.patron_real.match(self.codigo_fuente, self.posicion)
            if match_real and '.' in match_real.group(0):
                self.tokens.append((Terminal('real', match_real.group(0)), 2))
                self.posicion = match_real.end()
            elif match_entero:
                self.tokens.append((Terminal('entero', match_entero.group(0)), 1))
                self.posicion = match_entero.end()
            else:
                raise Exception(f"Error léxico: Caracter inesperado '{self.codigo_fuente[self.posicion]}' en la posición {self.posicion}")
        else:
            match = None
            for patron, tipo in [(self.patron_operador, 'operador'), (self.patron_parentesis, 'parentesis'), 
                                 (self.patron_llave, 'llave'), (self.patron_punto_y_coma, 'punto_y_coma'),
                                 (self.patron_coma, 'coma'), (self.patron_igual, 'igual')]:
                match = patron.match(self.codigo_fuente, self.posicion)
                if match:
                    self.tokens.append((Terminal(tipo, match.group(0)), match.group(0)))
                    self.posicion = match.end()
                    break
            if not match:
                raise Exception(f"Error léxico: Caracter inesperado '{self.codigo_fuente[self.posicion]}' en la posición {self.posicion}")

    def obtener_tokens(self):
        return self.tokens

# Función de ejemplo
def ejemplo():
    pila = Pila()
    alumno = Licenciatura("345678", "Computacion", 200)
    pila.push(alumno)
    pila.push(Bachillerato("456789", "Preparatoria 12"))
    pila.push(Licenciatura("456789", "Informatica", 50))
    pila.muestra()
    print("*********************************")
    pila.pop()
    pila.muestra()

if __name__ == "__main__":
    # Ejemplo de uso
    codigo_fuente = """
    int a = 10;
    float b = 3.14;
    if (a > 5 && b < 4.0) {
        return a + b;
    } else {
        return a * b;
    }
    """

    analizador_lexico = AnalizadorLexico(codigo_fuente)
    analizador_lexico.analizar()
    tokens_resultantes = analizador_lexico.obtener_tokens()

    analizador_sintactico = AnalizadorSintactico(tokens_resultantes)
    analizador_sintactico.analizar()
