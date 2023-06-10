import argparse
from gensim.models import Word2Vec

parser = argparse.ArgumentParser(
    prog="Model Test",
    epilog="Made for SPLN 2022/2023"
)

parser.add_argument('model')
parser.add_argument('--analogy','-a', nargs=3, action='store')
parser.add_argument('--similarity','-s', nargs=2, action='store')
parser.add_argument('--most_similar','-m', nargs=1, action='store')

args = parser.parse_args()

model = Word2Vec.load(args.model)

if args.analogy:
    analogy = args.analogy
    m = model.wv.most_similar(positive=[analogy[0],analogy[2]], negative=[analogy[1]])
    print(f'{analogy[0]}  + {analogy[1]} = {analogy[2]} + ?')
    print('? = ',m)

if args.similarity:
    print(f"Similarity score: {model.wv.similarity(args.similarity[0],args.similarity[1])}")

if args.most_similar:
    print(f"Most similar to {args.most_similar[0]}: {model.wv.most_similar(args.most_similar[0])}")






