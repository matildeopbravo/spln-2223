#!/usr/bin/env python3
import sys
import fileinput
import re
import argparse
import sys

parser = argparse.ArgumentParser(description="Tokenize Book")
parser.add_argument("-l", "--lang", default="en", help="Language")
parser.add_argument(
    "input", metavar="filename", type=str, nargs="?", help="input file", default=None
)
args = parser.parse_args()
text = ""
chapters = {"pt": "CAP[ÍI]TULO", "en": "CHAPTER", "fr": "CHAPITRE", "es": "CAP[ÍI]TULO"}
poems = {"pt": "poema", "en": "poem", "fr": "po[èe]me", "es": "poema"}

if args.input:
    with open(args.input, "r", encoding="utf-8") as f:
        text = f.read()
else:
    for line in sys.stdin:
        text += line

# ^ é inicio da string (não linha) por default
# Marcar capitulos
regex_cap = rf".*({chapters[args.lang]} \w+).*\n(.*)"
text = re.sub(regex_cap, r"\n# \1 - \2 #", text)

# Remover Quebras de pagina
regex_nl = r"([a-z0-9,;\-])\n\n([a-z0-9])"
text = re.sub(regex_nl, r"\1\n\2", text)

# Dar tag a poemas
arr_poemas = []

def guarda_poema(poema):
    arr_poemas.append(poema)
    return f">> Poema {len(arr_poemas)} <<"


regex_poema = rf"<{poems[args.lang]}>(.*)</{poems[args.lang]}>"
text = re.sub(regex_poema, guarda_poema, text, flags=re.S)

# Separar pontuação das palavras
text = re.sub(r"(?i)(Sr|Sra)\.", lambda abv: abv.group(1).upper(), text)

### hifen=
ending_punct = r".!?;"
punct = ending_punct + ",:"
regex_pontuacao = rf"(\w)([{punct}]+)"
text = re.sub(regex_pontuacao, r"\1 \2", text)
#
### Separar parágrafos de linhas pequenas
## regex_10_palavras = r"^((?:\w+[^\w\n]){0,9}\w+\W+\n)"
### Menos de 10 palavras
## text = re.sub(regex_10_palavras, r"\1\nend_paragraph\n\n", text, flags=re.M)

## Juntar linhas da mesma frase
## Quebrar as frases (uma frase por linha)
def frase(match):
    x = re.sub("\n", " ", match[0])
    return x + "\n"


regex_frase = rf"(\w+)[^{ending_punct}#]* ([{ending_punct}]+)( |\n)?"
text = re.sub(regex_frase, frase, text, flags=re.M)

print(text)