import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import re
from enum import Enum

class TokenType(Enum):
    # Enumeración de tipos de token
    PalabraReservadaTrue = 0
    PalabraReservadaFalse = 1
    PalabraReservadaReturn = 2
    PalabraReservadaVoid = 3
    PalabraReservadaChar = 4
    PalabraReservadaShort = 5
    PalabraReservadaInt = 6
    PalabraReservadaLong = 7
    PalabraReservadaFloat = 8
    PalabraReservadaDo = 9
    PalabraReservadaWhile = 10
    PalabraReservadaFor = 11
    PalabraReservadaBreak = 12
    PalabraReservadaSwitch = 13
    PalabraReservadaIf = 14
    OperacionSuma = 15
    OperacionResta = 16
    OperacionIncremento = 17
    OperacionDecremento = 18
    OperacionMasIgual = 19
    OperacionMenosIgual = 20
    OperacionMultiplicacion = 21
    OperacionDivision = 22
    OperacionMultiplicacionIgual = 23
    OperacionDivisionIgual = 24
    OperacionModulo = 25
    OperacionModuloIgual = 26
    ANDBits = 27
    ANDLogico = 28
    ORBits = 29
    ORLogico = 30
    MayorQue = 31
    MenorQue = 32
    MayorIgualQue = 33
    MenorIgualQue = 34
    IgualA = 35
    DiferenteDe = 36
    Negacion = 37
    CorrimientoHaciaLaDerecha = 38
    CorrimientoHaciaLaIzquierda = 39
    Asignacion = 40
    Dolar = 41
    LlaveAbre = 42
    LlaveCierra = 43
    ParentesisAbre = 44
    ParentesisCierra = 45
    CorcheteAbre = 46
    CorcheteCierra = 47
    Coma = 48
    PuntoComa = 49
    Identificador = 50
    Numero = 51
    NumeroFlotante = 52
    Cadena = 53
    Desconocido = 54
    PalabraReservadaPrint = 55
    PalabraReservadaElse = 56

class Token:
    # Clase para representar un token
    def __init__(self, type: TokenType, lexema: str, line: int):
        self.type = type
        self.lexema = lexema
        self.line = line

    def __str__(self):
        return f'Token: {token_types[self.type.value][1]:<32s}Lexema: {self.lexema:<24s}Linea: {self.line}'

token_types = [
    # Definición de tipos de token
    ('true', 'Palabra reservada true'),
    ('false', 'Palabra reservada false'),
    ('return', 'Palabra reservada return'),
    ('void', 'Palabra reservada void'),
    ('char', 'Palabra reservada char'),
    ('short', 'Palabra reservada short'),
    ('int', 'Palabra reservada int'),
    ('long', 'Palabra reservada long'),
    ('float', 'Palabra reservada float'),
    ('do', 'Palabra reservada do'),
    ('while', 'Palabra reservada while'),
    ('for', 'Palabra reservada for'),
    ('break', 'Palabra reservada break'),
    ('switch', 'Palabra reservada switch'),
    ('if', 'Palabra reservada if'),
    ('+', 'Operacion suma'),
    ('-', 'Operacion resta'),
    ('++', 'Operacion incremento'),
    ('--', 'Operacion decremento'),
    ('+=', 'Operacion mas igual'),
    ('-=', 'Operacion menos igual'),
    ('*', 'Operacion multiplicacion'),
    ('/', 'Operacion division'),
    ('*=', 'Operacion multiplicacion igual'),
    ('/=', 'Operacion division igual'),
    ('%', 'Operacion modulo'),
    ('%=', 'Operacion modulo igual'),
    ('&', 'AND a nivel de bits'),
    ('&&', 'AND logico'),
    ('|', 'OR a nivel de bits'),
    ('||', 'OR logico'),
    ('>', 'Mayor que'),
    ('<', 'Menor que'),
    ('>=', 'Mayor o igual que'),
    ('<=', 'Menor o igual que'),
    ('==', 'Igual a'),
    ('!=', 'Diferente de'),
    ('!', 'Negacion'),
    ('>>', 'Corrimiento hacia la derecha'),
    ('<<', 'Corrimiento hacia la izquierda'),
    ('=', 'Asignacion'),
    ('$', 'Simbolo dolar'),
    ('{', 'Llave abre'),
    ('}', 'Llave cierra'),
    ('(', 'Parentesis abre'),
    (')', 'Parentesis cierra'),
    ('[', 'Corchete abre'),
    (']', 'Corchete cierra'),
    (',', 'Coma'),
    (';', 'Punto y coma'),
    ('', 'Identificador'),
    ('', 'Numero'),
    ('', 'Numero flotante'),
    ('', 'Cadena'),
    ('', 'Desconocido'),
    ('print', 'Palabra reservada print'),
    ('else', 'Palabra reservada else'),
]

class AnalizadorLexico:
    # Clase para realizar análisis léxico
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente
        self.tokens = []
        self.errores = []

    def analizar(self):
        pos = 0
        line = 1
        while pos < len(self.codigo_fuente):
            if self.codigo_fuente[pos].isspace():
                pos += 1
            elif self.codigo_fuente[pos].isdigit():
                # Analizar número entero o flotante
                match_entero = re.match(r'\d+', self.codigo_fuente[pos:])
                match_real = re.match(r'\d+\.\d+', self.codigo_fuente[pos:])
                if match_real:
                    valor = match_real.group(0)
                    self.tokens.append(Token(TokenType.NumeroFlotante, valor, line))
                    pos += len(valor)
                elif match_entero:
                    valor = match_entero.group(0)
                    self.tokens.append(Token(TokenType.Numero, valor, line))
                    pos += len(valor)
            elif self.codigo_fuente[pos].isalpha() or self.codigo_fuente[pos] == '_':
                # Analizar identificador
                match_identificador = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self.codigo_fuente[pos:])
                if match_identificador:
                    valor = match_identificador.group(0)
                    if valor in [item[0] for item in token_types]:
                        token_type = TokenType[valor.capitalize()]
                    else:
                        token_type = TokenType.Identificador
                    self.tokens.append(Token(token_type, valor, line))
                    pos += len(valor)
                else:
                    self.errores.append(f"Error léxico: Identificador no válido en la línea {line}")
                    pos += 1
            elif self.codigo_fuente[pos] in '+-*/=':
                # Analizar operadores
                self.tokens.append(Token(TokenType[self.codigo_fuente[pos]], self.codigo_fuente[pos], line))
                pos += 1
            elif self.codigo_fuente[pos] in '{}()[],;':
                # Analizar separadores
                self.tokens.append(Token(TokenType[self.codigo_fuente[pos]], self.codigo_fuente[pos], line))
                pos += 1
            elif self.codigo_fuente[pos] == '\n':
                # Incrementar contador de línea
                line += 1
                pos += 1
            else:
                # Carácter no reconocido
                self.errores.append(f"Error léxico: Caracter no reconocido en la línea {line}")
                pos += 1

class Index(tk.Tk):
    # Clase para la interfaz gráfica
    def __init__(self):
        super().__init__()
        self.title("Analizador de Código")
        self.geometry("800x600")

        self.frame_editor = tk.Frame(self)
        self.frame_editor.pack(fill=tk.BOTH, expand=True)

        self.label_editor = tk.Label(self.frame_editor, text="Introduce tu código:")
        self.label_editor.pack(side=tk.TOP)

        self.texto_editor = tk.Text(self.frame_editor, wrap=tk.WORD)
        self.texto_editor.pack(fill=tk.BOTH, expand=True)

        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(fill=tk.BOTH, expand=True)

        self.boton_cargar_excel = tk.Button(self.frame_botones, text="Cargar Excel", command=self.cargar_excel)
        self.boton_cargar_excel.pack(side=tk.LEFT)

        self.boton_compilar = tk.Button(self.frame_botones, text="Compilar", command=self.compilar)
        self.boton_compilar.pack(side=tk.LEFT)

        self.boton_analizar_lexico = tk.Button(self.frame_botones, text="Analizar Léxico", command=self.analizar_lexico)
        self.boton_analizar_lexico.pack(side=tk.LEFT)

        self.boton_analizar_sintactico = tk.Button(self.frame_botones, text="Analizar Sintáctico", command=self.analizar_sintactico)
        self.boton_analizar_sintactico.pack(side=tk.LEFT)

        self.boton_generar_arbol = tk.Button(self.frame_botones, text="Generar Árbol", command=self.generar_arbol)
        self.boton_generar_arbol.pack(side=tk.LEFT)

        self.frame_resultado = tk.Frame(self)
        self.frame_resultado.pack(fill=tk.BOTH, expand=True)

        self.label_resultado = tk.Label(self.frame_resultado, text="Resultado del análisis:")
        self.label_resultado.pack(side=tk.TOP)

        self.texto_resultado = tk.Text(self.frame_resultado, wrap=tk.WORD)
        self.texto_resultado.pack(fill=tk.BOTH, expand=True)

        self.tree_view = ttk.Treeview(self.frame_resultado, columns=('Lexema', 'Tipo', 'Línea'), show='headings')
        self.tree_view.heading('Lexema', text='Lexema')
        self.tree_view.heading('Tipo', text='Tipo')
        self.tree_view.heading('Línea', text='Línea')
        self.tree_view.pack(fill=tk.BOTH, expand=True)

    def cargar_excel(self):
        # Cargar archivo Excel y mostrar los datos en el árbol
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not file_path:
            return

        self.tree_view.delete(*self.tree_view.get_children())  # Limpiar árbol
        data = pd.read_excel(file_path)
        for index, row in data.iterrows():
            self.tree_view.insert('', 'end', values=(row[0], row[1], row[2]))

    def compilar(self):
        # Método para compilar el código (aún por implementar)
        pass

    def analizar_lexico(self):
        # Método para analizar léxicamente el código
        codigo_fuente = self.texto_editor.get("1.0", tk.END)
        analizador_lexico = AnalizadorLexico(codigo_fuente)
        analizador_lexico.analizar()

        self.texto_resultado.delete("1.0", tk.END)  # Limpiar resultado anterior
        self.texto_resultado.insert(tk.END, "Análisis léxico:\n")
        for token in analizador_lexico.tokens:
            self.texto_resultado.insert(tk.END, f"Token: {token.lexema} (Tipo: {token.type.name})\n")
        if analizador_lexico.errores:
            self.texto_resultado.insert(tk.END, "Errores encontrados:\n")
            for error in analizador_lexico.errores:
                self.texto_resultado.insert(tk.END, f"{error}\n")
        else:
            self.texto_resultado.insert(tk.END, "No se encontraron errores léxicos.")

    def analizar_sintactico(self):
        # Método para analizar sintácticamente el código (aún por implementar)
        pass

    def generar_arbol(self):
        # Método para generar el árbol (aún por implementar)
        pass

if __name__ == "__main__":
    app = Index()
    app.mainloop()
