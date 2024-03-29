# Retrieves all pokemon species descriptions, and returns a document (string)
import requests

def fetch(url):
    r = requests.get(url)
    return None if r.status_code != 200 else r.json()

class Pokemon:
    count = 807

    def __init__(self, id):
        self.url = f'http://pokeapi.co/api/v2/pokemon-species/{id}'
        self.name = fetch(self.url)['name']

    # Creates a description of the pokemon, based on the entries of various pokedex entries
    def describe(self):
        descriptions = set()
        data = fetch(self.url)
        for x in data['flavor_text_entries']:
            toReplace = {'é':'e', '—':'', '-':' ','\xad':''}
            if x['language']['name'] == 'en':
                x['flavor_text'] = x['flavor_text'].lower()
                for a, b in toReplace.items():
                    x['flavor_text'] = x['flavor_text'].replace(a,b)
                x['flavor_text'] = ' '.join(x['flavor_text'].split())
                descriptions |= {x['flavor_text']}
        return ' '.join(descriptions)

def test_Pokemon(r = False):
    pokemon = Pokemon(1)
    doc = pokemon.describe()
    return doc if r else None

from nltk import word_tokenize, SnowballStemmer, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

class Tokenize(list):

    def __init__(self, doc):
        punctuations = [",","(",")","[","]","{","}","#","@","!",":",";",".","?","’"]
        tokens = word_tokenize(doc.lower())
        for t in tokens:
            if t not in punctuations and not t.isdigit():
                self.append(t)

    def rm_stopwords(self):
        stop_words = set(stopwords.words('english'))
        return [t for t in self if not t in stop_words]

    def Snowball(self):
        newTokens = []
        for t in self.rm_stopwords():
            x = SnowballStemmer('english').stem(t)
            if x not in newTokens:
                newTokens.append(x)
        return newTokens

    def Porter(self):
        newTokens = []
        for t in self.rm_stopwords():
            x = PorterStemmer().stem(t)
            if x not in newTokens:
                newTokens.append(x)
        return newTokens

    def Lemmatize(self):
        newTokens = []
        for t in self.rm_stopwords():
            x = WordNetLemmatizer().lemmatize(t)
            if x not in newTokens:
                newTokens.append(x)
        return newTokens

## Testing
def test_Tokenize(r = False):
    doc = test_Pokemon(True)
    tokens = Tokenize(doc)
    print(f'Clean Tokens:\n\t{tokens}\n')
    print(f'No Stop Words:\n\t{tokens.rm_stopwords()}\n')
    print(f'Using Snowball Stemmer:\n\t{tokens.Snowball()}\n')
    print(f'Using Porter Stemmer:\n\t{tokens.Porter()}\n')
    print(f'Using WordNetLemmatizer:\n\t{tokens.Lemmatize()}\n')
    return tokens.rm_stopwords() if r else None

from math import log, log2

class Vectorize(dict):
    def __init__(self, tokens):
        for t in tokens:
            if t in self.keys():
                self[t] += 1
            else:
                self[t] = 1

    def tf(self):
        total = sum(self.values())
        return { t : v/total for t, v in self.items()}

    def log(self):
        return {t : log(1 + v) for t, v in self.items()}

    def dNorm(self, K):
        maxCount = max(self.values())
        return {t : K+(1-K)*(v/maxCount) for t, v in self.items()}

    def tfidf(self, iidx): #tf-idf score
        total = sum(self.values())  # total = sum of counts
        idf = iidx.idf()            # (term : idf)
        return {t : (v/total)*idf[t] for t, v in self.items()}

def test_Vectorize(r = False):
    tokens = test_Tokenize(True)
    dV = Vectorize(tokens)
    print(f'Count Vector:\n\t{dV}\n')
    print(f'Term-Freq Vector:\n\t{dV.tf()}\n')
    print(f'Log-Norm Vector:\n\t{dV.log()}\n')
    print(f'Double-Norm Vector (K = 0.5):\n\t{dV.dNorm(0.5)}\n')
    return dV if r else None

class InvertedIndex(dict):

    def add(self, vector, label):
        for t in vector.keys():
            if t in self.keys():
                self[t].append(label)
            else:
                self[t] = [label]
        return self

class IDF(dict):
    def __init__(self, iidx):
        numTerms = len(iidx)
        for t, v in iidx.items():
            self[t] = log2(numTerms/len(v))

    def score(self, doc, sQ):
        tD = Tokenize(doc) #HERE
        vD = Vectorize(tD).tf()
        score = 0
        for t in sQ:
            if t in vD.keys():
                score += vD[t]*self[t]
        return score

def test_InvertedIndex():
    iidx = InvertedIndex()
    print('--------------------------------------------------------------')
    for id in range(1,101):
        pokemon = Pokemon(id)
        doc = pokemon.describe()
        tokens = Tokenize(doc)  #HERE
        dV = Vectorize(tokens)
        iidx.add(dV, id)
        print(f'Scanning Pokemon {id:3}: {pokemon.name}')
    #print(f'Inverted Index after adding doc {id}:\n\t{iidx}\n')
    #print(f'this index has doc-freq:\n\t{iidx.idf()}\n')
    #print('Q = a small yellow pokemon that resembles a mouse')
    Q = 'electric type pokemons that are also ground type'
    #Q = 'It has small electric sacs on both its cheeks. If threatened, it looses electric charges from the sacs'
    sQ = set(Tokenize(Q)) #HERE
    idf = IDF(iidx)
    #print(f'IDF is:\n\t{idf}\n')
    for id in range(1,101):
        doc = Pokemon(id).describe()
        print(f'Score of Q in pokemon {id} is: {idf.score(doc, sQ)}')



test_InvertedIndex()
