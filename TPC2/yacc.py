import ply.yacc as yacc
from lex import tokens
import sys

# linha branco separa entradas
start = "Dic"
entradas = []


def p_Dic(p):
    "Dic : ListaEntr"
    pass


def p_ListaEntr_One(p):
    "ListaEntr : Entr"
    pass


def p_ListaEntr(p):
    "ListaEntr : ListaEntr Entr"
    pass

def p_ListNL(p):
    "ListNL : ListNL NL"
    pass


def p_ListNLEmpty(p):
    "ListNL :"
    pass

def p_Areas(p):
    "Areas : AREAS ListAreas NL"
    pass

def p_ListAreas(p):
    """ListAreas : TEXT
    | ListAreas ';' TEXT"""
    pass

def p_Entr(p):
    "Entr : ListNL id Areas Linguas"
    pass

def p_id(p):
    "id : ID NUMBER NL"
    pass

def p_Linguas(p):
    "Linguas : LANG NL Langs"


def p_Langs(p):
    """Langs : Lang
    | Langs Lang"""
    pass


def p_Lang(p):
    "Lang : ID_LING Val ListaAtrLing NL"
    pass


def p_ListaAtrLing(p):
    """ListaAtrLing :
    | ListaAtrLing AtrLing"""
    pass

def p_Atr(p):
    "AtrLing : NL PLUS ATR_LINGUA Val"
    pass

def p_Traducao(p):
    "Val : TEXT ListaAtrTermo"
    pass

def p_ListaAtrTermo(p):
    """ListaAtrTermo :
    | ListaAtrTermo ATR_TERMO """
    pass

def p_error(p):
    print("Syntax error: ", p)
    parser.success = False


# Build the parser
parser = yacc.yacc()

with open("exemplo.txt", "r") as f:
    content = f.read()
    parser.i = 0
    parser.success = True
    parser.flag = True
    parser.last = 0
    result = parser.parse(content)
    print(parser.success)
