# Retrieves all pokemon species descriptions, and returns a document (string)
import requests

def fetch(url):
    r = requests.get(url)
    return None if r.status_code != 200 else r.json()

class Pokemon:
    def __init__(self, id):
        self.url = f'http://pokeapi.co/api/v2/pokemon-species/{id}'

    # Creates a description of the pokemon, based on the entries of various pokedex entries
    def describe(self):
        descriptions = set()
        data = fetch(self.url)
        for x in data['flavor_text_entries']:
            toReplace = {'é':'e', '—':''}
            if x['language']['name'] == 'en':
                x['flavor_text'] = x['flavor_text'].lower()
                for a, b in toReplace.items():
                    x['flavor_text'] = x['flavor_text'].replace(a,b)
                x['flavor_text'] = ' '.join(x['flavor_text'].split())
                descriptions |= {x['flavor_text']}
        return ' '.join(descriptions)


from nltk import word_tokenize, SnowballStemmer, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

class Tokenize(list):

    def __init__(self, doc):
        punctuations = [",","(",")","[","]","{","}","#","@","!",":",";",".","?","’"]
        tokens = word_tokenize(doc)
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
def pokeapi_test():
    pokemon = Pokemon(12)
    doc = pokemon.describe()
    tokens = Tokenize(doc)
    print(f'Clean Tokens:\n\t{tokens}\n')
    print(f'No Stop Words:\n\t{tokens.rm_stopwords()}\n')
    print(f'Using Snowball Stemmer:\n\t{tokens.Snowball()}\n')
    print(f'Using Porter Stemmer:\n\t{tokens.Porter()}\n')
    print(f'Using WordNetLemmatizer:\n\t{tokens.Lemmatize()}\n')