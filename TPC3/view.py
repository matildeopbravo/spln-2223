class Dicionario:
    def __init__(self, entradas=[]):
        self.entradas = entradas

    def show(self):
        pagHTML = """<!DOCTYPE html>
        <html>
            <head>
                  <meta charset="UTF-8"/>
                  <title> Dicionário </title>
            </head>
            <body>
            """
        for entrada in self.entradas:
            pagHTML += entrada.show()
        pagHTML += " </body> </html>"
        return pagHTML


class Entrada:
    def __init__(self, index, areas, langs):
        self.index = index
        self.areas = areas
        self.langs = langs

    def show(self):
        pag = f"""
            <h3> Entrada {self.index} </h3>
            <p> <b> Areas: </b> {"".join(self.areas)} </p>
            <p> <b> Traduções: </b>
        """
        for lang in self.langs:
            pag += lang.show()
        return pag


class Lang:
    def __init__(self, lang_name, main_def, atributos):
        self.lang_name = lang_name
        self.main_def = main_def
        self.atributos = atributos

    def show(self):
        pag = f"""<p> <b>{self.lang_name}</b> {self.main_def}
                <ul>

        """
        for atr in self.atributos:
            pag += f"<li> {atr} </li>"
        pag += "</ul>"
        return pag
