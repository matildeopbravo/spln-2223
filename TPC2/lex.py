import ply.lex as lex

# LEXER

tokens = (
    "OPEN_FULL",
    "TEXT",
    "INDEX",
    "SEPARATOR",
    "OPEN_CAT",
    "OPEN_SIN",
    "OPEN_VAR",
    "OPEN_LANG",
    "OPEN_NOTE",
    "OPEN_REM",
    "OPEN_VID",
    "NEWLINE",
    "SEP_ENTRADA",
    "LANG",
)

w_c = r"A-Za-zÀ-ÖØ-öø-ÿ"
literals = ["[", "]", ":"]
t_ignore = " "

t_OPEN_FULL = r">"
t_TEXT = rf"(?<![{w_c}\[])[{w_c}]+(?:[ ]+[{w_c}]+)*(?![{w_c}:])"
t_INDEX = r"\d+"
t_SEPARATOR = r";"
t_OPEN_CAT = r"cat:"
t_OPEN_SIN = r"sin:"
t_OPEN_VAR = r"var:"
# t_OPEN_LANG = rf"(?<=\[)[{w_c}\.]+(?=\])"
t_LANG = r"(en|pt|es|la|ga):"
t_OPEN_NOTE = r"nota:"
t_OPEN_REM = r"\#"
t_OPEN_VID = r"vid:"
t_NEWLINE = r"\n(?!\n)"
t_SEP_ENTRADA = r"\n\n"


def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)
    t.lexer


lexer = lex.lex()
