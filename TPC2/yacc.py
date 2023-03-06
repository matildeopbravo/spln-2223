import ply.yacc as yacc
from lex import tokens
import sys

# linha branco separa entradas
start = "dic"


def p_1(p):
    "dic : entradas"
    print(p[1])


def p_2(p):
    "entradas : entrada LINHA_B entradas"
    p[0] = [p[1]] + p[3]
    print("entradas: ", p[0])


def p_3(p):
    "entradas : entrada"
    p[0] = p[1]


def p_4(p):
    "entrada : itens"
    p[0] = p[1]
    print("entrada => ", p[1])
    # print(p[0])


def p_5(p):
    "itens : item resto_itens"
    p[0] = p[1]
    print("itens")
    # print(p[0])


def p_resto_itens_1(p):
    "resto_itens : NEWLINE itens"
    p[0] = p[1] + p[2]
    # print(p[0])


def p_resto_itens_2(p):
    "resto_itens :"
    pass


def p_7(p):
    "item : at_conceito"
    p[0] = p[1]
    print(f"item: {parser.i}  => ", p[0])
    parser.i += 1


def p_9(p):
    "at_conceito : ID ':' VAL"
    p[0] = f"{p[1]}:{p[3]}"
    print("at_conceito", parser.i, p[0])
    parser.i += 1
    pass


# def p_8(p):
#    "item : lingua"
#    pass
#

# def p_8(p):
#    "item : lingua"
#    pass
#
# def p_10(p):
#    "lingua : ID_LING ':' NEWLINE ts"
#    pass
#
# def p_11(p):
#    "ts : ts t"
#    pass
#
# def p_12(p):
#    "ts : t"
#    pass
#
# def p_13(p):
#    "t : '-' VAL at_ts"
#    pass
#
# def p_14(p):
#    "at_ts : at_ts at_t"
#    pass
#
# def p_15(p):
#    "at_ts : "
#    pass
#
# def p_16(p):
#    "at_t : NEWLINE '+' ID ':' VAL "
#    pass
#
def p_error(p):
    print("Syntax error: ", p)
    parser.success = False


# Build the parser
parser = yacc.yacc()

with open("exemplo", "r") as f:
    content = f.read()
    parser.i = 0
    parser.success = True
    parser.flag = True
    parser.last = 0
    result = parser.parse(content)
