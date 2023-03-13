import ply.yacc as yacc
from lex import tokens
import sys
import view

# linha branco separa entradas
start = "Dic"
entradas = []


def p_Dic(p):
    "Dic : ListaEntr"
    p[0] = view.Dicionario(p[1])
    print(p[0].show())
    pass


def p_ListaEntr_One(p):
    "ListaEntr : Entr"
    p[0] = [p[1]]
    pass


def p_ListaEntr(p):
    "ListaEntr : ListaEntr Entr"
    p[0] = p[1] + [p[2]]
    pass


def p_ListNL(p):
    "ListNL : ListNL NL"
    pass


def p_ListNLEmpty(p):
    "ListNL :"
    pass


def p_Areas(p):
    "Areas : AREAS ListAreas NL"
    p[0] = p[2]
    pass


def p_ListAreas_One(p):
    "ListAreas : TEXT"
    p[0] = [p[1]]


def p_ListAreas(p):
    "ListAreas : ListAreas ';' TEXT"
    p[0] = p[1] + [p[3]]


def p_Entr(p):
    "Entr : ListNL id Areas Linguas"
    p[0] = view.Entrada(p[2], p[3], p[4])
    pass


def p_id(p):
    "id : ID NUMBER NL"
    p[0] = p[2]
    pass


def p_Linguas(p):
    "Linguas : LANG NL Langs"
    p[0] = p[3]


def p_Langs_One(p):
    "Langs : Lang"
    p[0] = [p[1]]


def p_Langs(p):
    "Langs : Langs Lang"
    p[0] = p[1] + [p[2]]


def p_Lang(p):
    "Lang : ID_LING Val ListaAtrLing NL"
    p[0] = view.Lang(p[1], p[2], p[3])
    pass


def p_ListaAtrLing_Empty(p):
    "ListaAtrLing :"
    p[0] = []
    pass


def p_ListaAtrLing(p):
    "ListaAtrLing : ListaAtrLing AtrLing"
    p[0] = p[1] + [p[2]]


def p_Atr(p):
    "AtrLing : NL PLUS ATR_LINGUA Val"
    p[0] = p[3] + ": " + p[4]


def p_Traducao(p):
    "Val : TEXT ListaAtrTermo"
    p[0] = p[1] + p[2]
    pass


def p_ListaAtrTermo_Empty(p):
    "ListaAtrTermo :"
    p[0] = ""
    pass


def p_ListaAtrTermo(p):
    "ListaAtrTermo : ListaAtrTermo ATR_TERMO"
    p[0] = p[1] + p[2]
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
