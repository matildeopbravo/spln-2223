import re
from re import Match, finditer, search
from typing import Optional, TypedDict
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
    langs: dict[str, str]
    note: str

    rem_entries: Optional[list[RemissiveEntry]]

    def __init__(self, id: int, name: str, name_types: list[str]):
        self.name = name
        self.id = id
        self.syn = []
        self.variants = []
        self.name_types = name_types
        self.categories = []
        self.langs = {}
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
        # improve this
        langs = []
        for k in self.langs:
            langs.append(f"{k} => {self.langs[k]}")
        s += "\n".join(langs)

        s = re.sub(" +", " ", s)
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
    regex_lang = r"\s*(es|en|pt|la)\s*"
    curr_entry.categories = re.findall(categories_regex, match_italic.group(1))
    content = next(it).group(1)
    while sin_var_match := re.match(r"\s*(SIN|VAR).-(.*)\s*", content):
        # either_sin_var = sin_var_match.group(2).split(";")
        sin_var_content = sin_var_match.group(2)
        if sin_var_match.group(1) == "SIN":
            sin_string = sin_var_content
            content = next(it).group(1)
            while not re.match(regex_lang, content) and not re.search(
                r"VAR.-", content
            ):
                sin_string += content
                content = next(it).group(1)
            curr_entry.syn = sin_string.split(";")
        elif sin_var_match.group(1) == "VAR":
            sin_string = sin_var_content
            content = next(it).group(1)
            while not re.match(regex_lang, content):
                sin_string += content
                content = next(it).group(1)
            curr_entry.variants = sin_string.split(";")

        # print(f"{curr_entry.syn}  e  {curr_entry.variants}")
    while language_name_match := re.match(regex_lang, content):
        lang = language_name_match.group(1)
        curr_entry.langs[lang] = ""
        content = next(it).group(1)
        is_colon = False
        while translation := re.match(r"<i>(.*)</i>", content) or (
            is_colon := re.match(r"\s*;\s*", content)
        ):
            if is_colon:
                curr_entry.langs[lang] += "; "
            else:
                curr_entry.langs[lang] += translation.group(1)
            content = next(it).group(1)
            is_colon = False

    return curr_entry


def parse_data(data: str):
    priv_entries = {}
    it = finditer(r"<text.*?>(.*\S+.*)</text>", data)
    for match in it:
        between_text = match.group(1)
        if is_useful(between_text):
            is_entry_header = re.match(
                r"<b>\s*(\d+)\s*(.+?)\s+((?:\w+ )*\w+)</b>", between_text
            )
            if is_entry_header:
                try:
                    # print(is_entry_header.group(1) + "=>" + is_entry_header.group(2))
                    entry = parse_full_entry(is_entry_header, it)
                    priv_entries[entry.id] = entry
                except StopIteration:
                    return priv_entries

    return entries


with open("medicina.xml", encoding="utf-8") as f:
    data = f.read()
    entries = parse_data(data)

    while True:
        n = int(input("What entry would you like to see? "))
        if n in entries:
            print(entries[n])
        else:
            print("Entry not found")
