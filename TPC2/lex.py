import ply.lex as lex

literals = [":", "-", "+", "$"]

tokens = ("ID", "ID_LING", "VAL", "LINHA_B", "NEWLINE")


# pode ser definição
def t_ID(t):
    r"\w+(?=:)"
    return t


def t_ID_LING(t):
    r"(en|pt|es|la|ga)(?=:)"


def t_LINHA_B(t):
    r"\n\n"
    return t


def t_VAL(t):
    r"[\w ]+"
    return t


def t_NEWLINE(t):
    r"\n(?!\n)"
    return t


# "def t_EOF(t):
# "    r"\$"
# "    return t


t_ignore = "\t"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

# lexer.input("id: 543\nNota: ola isto e uma nota\n")
#
# while True:
#    tok = lexer.token()
#    print(tok)
#    if not tok:
#        print("no tok")
#        break
