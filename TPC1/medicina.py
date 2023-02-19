import re
import json

texto = open("medicina.xml", "r").read()


def remove_header_footer(texto):
    texto = re.sub(r"<text.*>V.*\n.*ocabulario.*\n.*<\/text>", "", texto)
    texto = re.sub(r".*\n###\n.*\n", r"", texto)
    texto = re.sub(r"<page.*\n|</page>\n", r"", texto)

    return texto


texto = remove_header_footer(texto)


def marcaE(texto):
    texto = re.sub(r'<text.* font="3"><b>\s*(\d+\s+.*)</b></text>', r"###C \1", texto)
    texto = re.sub(r'<text.* font="8"><b>\s*(.*)\s*</b></text>', r"###R \1", texto)
    texto = re.sub(r'<text.* font="3"><b>\s*(\S.*)</b></text>', r"###R \1", texto)
    texto = re.sub(r'<text.* font="11"><b>\s*(\S.*)</b></text>', r"###R \1", texto)
    return texto


texto = marcaE(texto)


def limpeza(texto):
    texto = re.sub(r'<text.* font="4">.*</text>', r"", texto)
    texto = re.sub(r'<text.* font="3">.*</text>', r"", texto)
    texto = re.sub(r"<text[^<]*?>\s*<\/text>", r"", texto)
    texto = re.sub(r"<text[^<]*?>\s*<b>\s*</b>\s*<\/text>", r"", texto)
    return texto


texto = limpeza(texto)


def marcaLinguas(texto):
    texto = re.sub(r'<text.* font="0">\s*(\S+)\s*</text>', r"@ \1", texto)
    texto = re.sub(r"@ ;", r";", texto)
    texto = re.sub(r'<text.* font="7"><i>(.*)</i></text>', r"\1", texto)
    return texto


texto = marcaLinguas(texto)


def marcaSIN_VAR(texto):
    texto = re.sub(r'<text.* font="5">\s*(SIN.*)</text>', r"@\1", texto)
    texto = re.sub(r'<text.* font="0">\s*(SIN.*)</text>', r"@\1", texto)
    texto = re.sub(r'<text.* font="5">\s*(VAR.*)</text>', r"@\1", texto)
    texto = re.sub(r'<text.* font="0">\s*(VAR.*)</text>', r"@\1", texto)
    return texto


texto = marcaSIN_VAR(texto)


def marcaArea(texto):
    texto = re.sub(r'<text.* font="6"><i>\s*(.*)\s*</i></text>', r"% \1", texto)
    return texto


texto = marcaArea(texto)


def marcaVid(texto):
    texto = re.sub(r'<text.* font="\d*">\s*(Vid\..*)</text>', r"\1", texto)
    return texto


texto = marcaVid(texto)


def limpaFontSpec(texto):
    texto = re.sub(r"<fontspec.*\n", r"", texto)
    return texto


texto = limpaFontSpec(texto)


def marcaNota(texto):
    texto = re.sub(r'<text.* font="9">(.*)</text>', r".\1", texto)
    return texto


texto = marcaNota(texto)


def replace_values(texto):
    texto = re.sub(r'<text.* font="5">(.*)</text>', r"\1", texto)
    texto = re.sub(r'<text.* font="10"><i><b>(.*)</b></i></text>', r"\1", texto)
    return texto


texto = replace_values(texto)


def fix_formatting(texto):
    texto = re.sub(
        r'<text.* font="\d+">\s*(\d+)\s*</text>\n###R(.*)', r"###C \1 \2", texto
    )
    return texto


texto = fix_formatting(texto)


def formulaQuimica(texto):
    texto = re.sub(r'<text.* font="13"><b>\s*(\d+)\s*</b></text>', r"_\1", texto)
    texto = re.sub(r'<text.* font="15"><i>\s*(\d+)\s*</i></text>', r"_\1", texto)
    texto = re.sub(r'<text.* font="14">\s*(\d+)\s*</text>', r"_\1", texto)
    return texto


texto = formulaQuimica(texto)


def end(texto):
    texto = re.sub(r'<text.* font="0">\s*(\S.*)</text>', r"\1", texto)
    texto = re.sub(r"###R\s*\n", r"", texto)
    texto = re.sub(r"</pdf2xml>\s*", r"", texto)
    return texto


texto = end(texto)


def troca_entradas(texto):
    texto1 = ""

    texto = re.sub(r"###C (\d+)\s*\n(.*)", r"###C \1 \2", texto)

    while texto != texto1:
        texto1 = texto
        texto = re.sub(r"###C (.*)\s*###R (.*)", r"###C \1\2", texto)
        if texto == texto1:
            texto = re.sub(r"###C (\d+)\s*\n(.*)", r"###C \1 \2", texto)

    texto = re.sub(r"###C (.*)\n([^%@]*\n)###R", r"###C \1\2", texto)
    texto = re.sub(r"###C (.*)\n[^%]([fm])", r"###C \1 \2", texto)

    texto = re.sub(r"###C (.*)\n([^%]*)?\n@", r"###C \1\n% \2\n@", texto)
    return texto


texto = troca_entradas(texto)


def processa_areas(texto):
    return re.sub(r"%((?: [A-zÀ-ú]+)+) +((?: [A-zÀ-ú]+)+)", r"% \1;\2", texto)


texto = processa_areas(texto)


def processa_titulo_EC(texto):
    return re.sub(
        r"(###(?:C|E)) (\d+)\s+(\S+(?:\s\S+)*)((?: +\w+)+)",
        r"\1 \2;\3;\4",
        texto,
    )


texto = processa_titulo_EC(texto)


def get_lang(entry):
    m = re.match("\s*(es|en|pt|la)\n", entry)
    if m:
        return m.group(1)
    else:
        return None


# dicionario
dic = {"EC": {}, "ER": {}}

with open("medicina.txt", "w") as txt_file:
    txt_file.write(texto)

for e in texto.split("###")[1:]:
    if e[0] == "R":
        e = e[1:].split("\n")
        designacao = e[0].strip()
        referencia = re.sub(" +", " ", " ".join(e[1:]).strip())
        dic["ER"][designacao] = referencia
    elif e[0] == "C":
        e, *linguas = e[1:].split("@")
        e = [line for line in e[1:].split("\n") if line != ""]
        [iden, nome, cats] = e[0].split(";")
        areas = e[1][2:].split(";")
        areas = [a.strip() for a in areas]
        iden = iden.strip()
        dic["EC"][iden] = {
            "nome": nome.strip(),
            "categorias_gramaticais": cats.strip().split(),
            "areas": areas,
            "traducoes": {},
        }
        for entry in linguas[:-1]:
            lang = get_lang(entry)
            if lang:
                dic["EC"][iden]["traducoes"][lang] = [
                    s for s in entry.strip().split("\n")[1:] if s not in ("", ";")
                ]
            else:
                dic["EC"][iden]["sin_var"] = entry.strip()
        match = re.search(r"Nota.-(.*)", linguas[-1])
        if match:
            dic["EC"][iden]["nota"] = match.group(1)
        else:
            lang = get_lang(linguas[-1])
            if lang:
                dic["EC"][iden]["traducoes"][lang] = [
                    s for s in linguas[-1].strip().split("\n")[1:] if s not in ("", ";")
                ]


with open("medicina.json", "w", encoding="utf8") as json_file:
    json.dump(dic, json_file, indent=8, ensure_ascii=False)
