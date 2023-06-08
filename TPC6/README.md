# Web Scraping de Notícias

Este trabalho consistiu no desenvolvimento de um *script* cujo objetivo é fazer
*scraping* ao site de notícias do JN (Jornal de Notícias), com a utilização do
*package* **newspaper3k**.

## Procedimento
O *script* desenvolvido cria uma pasta com o nome correspondente à data atual, se esta não existir. Similarmente, caso esta não exista,  irá criar a pasta `news` que
    contém as pastas relativas a cada um dos dias em que foi executado. Será criado um ficheiro **xml** por todos os artigos obtidos, colocado na pasta correspondente ao dia em que executou. Além disso, também é criado um ficheiro de *log* que contém algumas informações sobre o processo.
    O utilizador deverá especificar uma pasta onde será criada a pasta *news* e as restantes subpastas.

## Execução Periódica
Para executar o *script* de forma periódica, por exemplo, diariamente, poderá ser criada um *cron job*.

Para abrir o ficheiro *crontab* dever-se-á executar o seguinte comando:
```sh
crontab -e
```
De seguida, deverá adicionar uma linha que indica o *script* a ser executado e a frequência com que este será executado.
```sh
	0 2 * * * path_to_script/scraper.py
```
Por exemplo, esta linha faria com que o *cron job* fosse executado todos os dias às 2 da manhã.
