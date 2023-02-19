import re
from re import Match, finditer, search
from typing import Optional
from collections.abc import Iterator
from abc import ABC


class Entry(ABC):
    name: str
    syn: list[str]
    variants: list[str]

    def __init__(self, name: str, syn: list[str], variants: list[str]):
        self.name = name
        self.syn = syn
        self.variants = variants


class RemissiveEntry(Entry):
    def __init__(self, name: str, syn: list[str]):
        super().__init__(name, syn, [])


class FullEntry(Entry):
    id: int
    name_types: list[str]  # a => adjective, f = feminine, m = masculine, pl => plural)
    categories: list[str]
    es: str
    en: str
    pt: str
    la: str
    note: str

    rem_entries: Optional[list[RemissiveEntry]]

    def __init__(self, id: int, name: str, name_types: list[str]):
        self.name = name
        self.id = id
        self.syn = []
        self.variants = []
        self.name_types = name_types
        self.categories = []
        self.es = ""
        self.en = ""
        self.pt = ""
        self.la = ""
        self.note = ""

    def __str__(self) -> str:
        s = f"{self.id} {self.name}     "
        for name_type in self.name_types:
            s += f" {name_type}"
        s += "\n"
        s += ";".join(self.categories)
        s += "\n"
        if self.syn:
            s += "SIN.-" + ";".join(self.syn) + "\n"
        if self.variants:
            if self.syn:
                s += "\n"
            s += "VAR.-" + ";".join(self.variants) + "\n"
        langs = ["es " + self.es, "en " + self.en, "pt " + self.pt, "la " + self.la]
        s += "\n".join(langs)

        return s


def is_useful(content: str):
    page_number_match = re.search(r"\s*\d+\s*$", content)
    return content != "V" and content != "ocabulario" and not page_number_match


def parse_full_entry(header_match: Match, it: Iterator):
    id = int(header_match.group(1))
    name = header_match.group(2)
    type = header_match.group(3)
    curr_entry = FullEntry(id, name, type.split())

    content = next(it).group(1)  # between <text>
    categories_regex = r"[A-zÀ-ú]+(?:\s[A-zÀ-ú]+)*"
    while not (match_italic := re.match(r"<i>(.*\w+.*)<\/i>", content)):
        rest_content = re.match(r"<(?:b|i)>(.*)</(?:b|i)>", content)
        if rest_content:
            # ver por causa do tipo at the end
            curr_entry.name += rest_content.group(1)
        content = next(it).group(1)

    # se for italico com algo la dentro entao vamos buscar as categorias
    curr_entry.categories = re.findall(categories_regex, match_italic.group(1))
    content = next(it).group(1)
    while sin_var_match := re.match(r"\s*(SIN|VAR).-(.*)\s*", content):
        either_sin_var = sin_var_match.group(2).split(";")
        if sin_var_match.group(1) == "SIN":
            curr_entry.syn = either_sin_var
        else:
            curr_entry.variants = either_sin_var
        # print(f"{curr_entry.syn}  e  {curr_entry.variants}")
        content = next(it).group(1)

    print(curr_entry, end="\n\n")

    return curr_entry


def parse_data(data: str):
    entries = {}
    it = finditer(r"<text.*?>(.*\S+.*)</text>", data)
    for match in it:
        between_text = match.group(1)
        if is_useful(between_text):
            is_entry_header = re.match(
                r"<b>\s*(\d+)\s*(.+?)\s+((?:\w+ )*\w+)</b>", between_text
            )
            if is_entry_header:
                # print(is_entry_header.group(1) + "=>" + is_entry_header.group(2))
                entry = parse_full_entry(is_entry_header, it)
                entries[entry.id] = entry

    return entries


with open("medicina.xml", encoding="utf-8") as f:
    data = f.read()
    entries = parse_data(data)

    while True:
        n = int(input("What entry would you like to see?"))
        if n in entries:
            print(entries[n])
        else:
            print("Entry not found")
