## Creates an inverted index, by continously extending itself when a new document vector is given

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