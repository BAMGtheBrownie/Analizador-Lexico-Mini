import tkinter as tk
from tkinter import filedialog
import openpyxl
import re


class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo  # Tipo del token (entero, real, operador, identificador, etc.)
        self.valor = valor  # Valor del token


class AnalizadorLexico:
    def __init__(self, codigo_fuente):
        self.codigo_fuente = codigo_fuente  # Código fuente a analizar
        self.patron_entero = r'\d+'  # Patrón para reconocer enteros
        self.patron_real = r'\d+\.\d+'  # Patrón para reconocer números reales
        self.patron_operadores = r'[+\-*/=]'  # Patrón para reconocer operadores
        self.patron_identificador = r'[a-zA-Z_][a-zA-Z0-9_]*'  # Patrón para reconocer identificadores
        self.caracteres_especiales = r'´+}{\[ \]!1|\"#$%&/()=?¡'  # Caracteres especiales
        self.tokens = []  # Lista para almacenar los tokens encontrados
        self.errores = []  # Lista para almacenar los errores léxicos encontrados

    def analizar(self):
        pos = 0
        while pos < len(self.codigo_fuente):
            if self.codigo_fuente[pos].isspace():
                pos += 1
            elif self.codigo_fuente[pos].isdigit():
                match_entero = re.match(self.patron_entero, self.codigo_fuente[pos:])
                if match_entero:
                    valor = match_entero.group(0)
                    self.tokens.append(Token('entero', valor))
                    pos += len(valor)
            elif self.codigo_fuente[pos] == '.':
                match_real = re.match(self.patron_real, self.codigo_fuente[pos:])
                if match_real:
                    valor = match_real.group(0)
                    self.tokens.append(Token('real', valor))
                    pos += len(valor)
            elif self.codigo_fuente[pos] in '+-*/=':
                self.tokens.append(Token('operador', self.codigo_fuente[pos]))
                pos += 1
            elif self.codigo_fuente[pos].isalpha() or self.codigo_fuente[pos] == '_':
                match_identificador = re.match(self.patron_identificador, self.codigo_fuente[pos:])
                if match_identificador:
                    valor = match_identificador.group(0)
                    self.tokens.append(Token('identificador', valor))
                    pos += len(valor)
            elif self.codigo_fuente[pos] in self.caracteres_especiales:
                # Agregar el carácter especial como un token
                self.tokens.append(Token('caracter_especial', self.codigo_fuente[pos]))
                pos += 1
            else:
                # Si no se reconoce el carácter, se agrega un mensaje de error a la lista de errores
                self.errores.append(f"Error léxico: Caracter no reconocido en la posición {pos}")
                pos += 1


def analizar_codigo():
    codigo_fuente = texto_entrada.get("1.0", tk.END)
    if codigo_fuente.strip():
        analizador_lexico = AnalizadorLexico(codigo_fuente)
        analizador_lexico.analizar()
        # Comparar tokens con datos del archivo Excel
        wb = openpyxl.load_workbook("compilador.xlsx")
        sheet = wb.active
        tokens_validos = [cell.value for cell in sheet["A"]]
        texto_salida.delete("1.0", tk.END)
        texto_errores.delete("1.0", tk.END)
        texto_salida.insert(tk.END, "Tokens encontrados:\n")
        for token in analizador_lexico.tokens:
            if token.valor in tokens_validos:
                texto_salida.insert(tk.END, f"Token válido: {token.valor} (Tipo: {token.tipo})\n")
            else:
                texto_salida.insert(tk.END, f"Token inválido: {token.valor} (Tipo: {token.tipo})\n")
        if analizador_lexico.errores:
            texto_errores.insert(tk.END, "Errores encontrados:\n")
            for error in analizador_lexico.errores:
                texto_errores.insert(tk.END, f"{error}\n")
        else:
            texto_errores.insert(tk.END, "No se encontraron errores léxicos.")


# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Analizador de Código")
root.geometry("800x600")

# Frame para la entrada de código
frame_entrada = tk.Frame(root)
frame_entrada.pack(fill=tk.BOTH, expand=True)

label_entrada = tk.Label(frame_entrada, text="Introduce tu código:")
label_entrada.pack(side=tk.TOP)

texto_entrada = tk.Text(frame_entrada, wrap=tk.WORD)
texto_entrada.pack(fill=tk.BOTH, expand=True)

# Frame para los botones
frame_botones = tk.Frame(root)
frame_botones.pack(fill=tk.BOTH, expand=True)

boton_analizar = tk.Button(frame_botones, text="Analizar código", command=analizar_codigo)
boton_analizar.pack()

# Frame para la salida del análisis
frame_salida = tk.Frame(root)
frame_salida.pack(fill=tk.BOTH, expand=True)

label_salida = tk.Label(frame_salida, text="Resultado del análisis:")
label_salida.pack(side=tk.TOP)

texto_salida = tk.Text(frame_salida, wrap=tk.WORD)
texto_salida.pack(fill=tk.BOTH, expand=True)

# Frame para los errores encontrados
frame_errores = tk.Frame(root)
frame_errores.pack(fill=tk.BOTH, expand=True)

label_errores = tk.Label(frame_errores, text="Errores encontrados:")
label_errores.pack(side=tk.TOP)

texto_errores = tk.Text(frame_errores, wrap=tk.WORD)
texto_errores.pack(fill=tk.BOTH, expand=True)

root.mainloop()
