## Tokenization procedure for any given document
from nltk import word_tokenize, SnowballStemmer, PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords

class Tokenize(list):
    # Default: removal of punctuations
    def __init__(self, doc):
        punctuations = [",","(",")","[","]","{","}","#","@","!",":",";",".","?","’"]
        tokens = word_tokenize(doc.lower())
        for t in tokens:
            if t not in punctuations and not t.isdigit():
                self.append(t)

    # Removal of stopwords
    def rm_stopwords(self):
        stop_words = set(stopwords.words('english'))
        return [t for t in self if not t in stop_words]

    # Stemming by SnowballStemmer post removal of stopwords
    def Snowball(self):
        newTokens = []
        for t in self.rm_stopwords():
            x = SnowballStemmer('english').stem(t)
            if x not in newTokens:
                newTokens.append(x)
        return newTokens

    # Stemming by PorterStemmer post removal of stopwords
    def Porter(self):
        newTokens = []
        for t in self.rm_stopwords():
            x = PorterStemmer().stem(t)
            if x not in newTokens:
                newTokens.append(x)
        return newTokens

    # Lemmatization by WordNetLemmatizer post removal of stopwords
    def Lemmatize(self):
        newTokens = []
        for t in self.rm_stopwords():
            x = WordNetLemmatizer().lemmatize(t)
            if x not in newTokens:
                newTokens.append(x)
        return newTokens

## Testing file
def testing():
    Q = 'It can go for days without eating a single morsel. In the bulb on its back, it stores energy.'
    tokens = Tokenize(Q)
    print(f'Clean Tokens:\n\t{tokens}\n')
    print(f'No Stop Words:\n\t{tokens.rm_stopwords()}\n')
    print(f'Using Snowball Stemmer:\n\t{tokens.Snowball()}\n')
    print(f'Using Porter Stemmer:\n\t{tokens.Porter()}\n')
    print(f'Using WordNetLemmatizer:\n\t{tokens.Lemmatize()}\n')
