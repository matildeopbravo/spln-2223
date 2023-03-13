import ply.lex as lex
import sys

literals = [":", "-", "+", "$", ";"]

tokens = (
    "ID",
    "AREAS",
    "LANG",
    "ID_LING",
    "TEXT",
    "NL",
    "PLUS",
    "NUMBER",
    "ATR_LINGUA",
    "ATR_TERMO",
)

# atributo de traducao
def t_ATR_LINGUA(t):
    r"syn|var|nota"
    return t


def t_ATR_TERMO(t):
    r"\((Br\.|Pt\.|pop\.|m|f|pl|sg)\)"
    return t


def t_ID(t):
    r"Id:"
    return t


def t_AREAS(t):
    r"Areas:"
    return t


def t_LANG(t):
    r"Lang:"
    return t


def t_ID_LING(t):
    r"(en|pt|es|la|ga):"
    return t


def t_NUMBER(t):
    r"\d+"
    return t


def t_TEXT(t):
    r"[^\n\+;\(\)]+"
    return t


def t_NL(t):
    r"\n"
    return t


def t_PLUS(t):
    r"\+"
    return t


t_ignore = " \t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

# file = open(sys.argv[1], "r")
# file = open("exemplo.txt", "r")
# program = file.read()
# lexer.input(program)
# for token in lexer:
#    print(token)
