# TPC1
## Utilização
```sh
python medicina.py
```
Após a utilização deste comando, são gerados o ficheiro **medicina.txt**, que corresponde à linguagem intermédia, e o ficheiro **medicina.json** com os dados correspondentes às entradas completas e remissivas.

## Criação do ficheiro medicina.xml

A partir do dicionário em pdf, foi gerado o seu correspondente em XML, já removendo alguma informação irrelevante do ficheiro, através do comando:
```sh
pdftohtml -f 20 -l 543 -xml medicina.pdf
```