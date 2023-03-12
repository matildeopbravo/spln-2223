class Dicionario:
    def __init__(self, entradas=[]):
        self.entradas = entradas

    def showDic(self):
        print("Dicionário")
        for entrada in self.entradas:
            entrada.show()

class Entrada:
    def __init__(self, index, areas, langs) :
        self.index = index
        self.areas = areas
        self.langs = langs

    def show(self):
        print(f"Id: {self.index} ")
        print(f"Areas: {self.areas} ")
        print("Traduções:")
        for lang in self.langs:
            lang.show()


class Lang:
    def __init__(self, lang_name, main_def, atributos):
        self.lang_name = lang_name
        self.main_def = main_def
        self.atributos = atributos

    def show(self):
        print(f"{self.lang_name}: {self.main_def}")
        for atr in self.atributos:
            print("\t\t" + atr)
