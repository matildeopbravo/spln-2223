import argparse

from gensim.models import Word2Vec
from gensim.utils import tokenize
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(
    prog="Criar Modelo",
    epilog="Made for SPLN 2022/2023"
)

parser.add_argument('-i','--input',default='corpus.html', action='store', type=str, nargs='*')
parser.add_argument('-e','--epochs',default=25)
parser.add_argument('-d','--dimension',default=300)
parser.add_argument('-o','--output',default='model')

args = parser.parse_args()

input_files = args.input
epochs = args.epochs
dim = args.dimension
out = args.output

aggregated_news = []

for file in input_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, features='lxml')
        for text in soup.find_all('article'):
            text = text.get_text()
            for line in text.splitlines():
                aggregated_news.append(list(tokenize(line, lowercase=True)))



model = Word2Vec(aggregated_news,epochs=epochs, vector_size=dim)

model.save(f'{out}.vec')
