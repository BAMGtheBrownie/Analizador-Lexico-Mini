# lexer.py

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
        return f'Token: {token_types[self.type.value][1]:
