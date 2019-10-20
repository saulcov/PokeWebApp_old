## Creates an inverted index, by continously extending itself when a new document vector is given
#  it also turns itself into a pickle, a pickle! (when closed).
from math import log
import pickle

class InvertedIndex(dict):

    def add(self, vector, label):
        for t in vector.keys():
            if t in self.keys():
                self[t].append(label)
            else:
                self[t] = [label]
        return self

    # I'M A PICKLE! I'm pickle Riiiiiick!
    def close(self, name):
        pickle_out = open(f'{name}.pickle', 'wb')
        pickle.dump(self, pickle_out)
        pickle_out.close()
    
## Testing file
def testing():
    # Doc A: 'it is what it is'
    A = {'it':2, 'is':2, 'what':1}
    # Doc B: 'what is it'
    B = {'what':1, 'is':1, 'it':1}
    # Doc C: 'it is a pickle'
    C = {'it':1, 'is':1, 'a':1, 'pickle':1 } 
    iidx = InvertedIndex()
    iidx.add(A, 'A')
    iidx.add(B, 'B')
    iidx.add(C, 'C')
    iidx.close('test_sample')
    print("I'm a pickle!")

def testing2():
    pickle_in = open('test_sample.pickle', 'rb')
    iidx = pickle.load(pickle_in)
    pickle_in.close()
    print('Anti-pickle serum!')
    print(iidx)
