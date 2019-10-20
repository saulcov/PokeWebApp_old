# PokeWebApp
A pokemon web app, implementing data mining techniques.

PokeAPI.py
Is used to interface with the PokeAPI (https://pokeapi.co/) and is used to generate a description of a given pokemon by merging the various descriptions of the pokemon found in different games/regions. For example run function sample_doc(1)

Tokenization.py
Is used to tokenize a given document by removing punctuation (default). It can also be used to remove stopwords, stem, or lemmmatize a document. For example run function testing()

Vectorization.py
Is used to turn an array of tokens to a dictionary, which will be treated as a vector, by default it returns a dictionary (token : raw count). Can also provide other common term-frequency measures such as: relative frequency, log normalization, and double k-normalization. As defined on (https://en.wikipedia.org/wiki/Tf–idf)