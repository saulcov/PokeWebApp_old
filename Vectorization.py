## Vectorizes an array of tokens based on term count by default
from math import log

class Vectorize(dict):
    # Default: pairs a token to its raw count on the array
    def __init__(self, tokens):
        for t in tokens:
            if t in self.keys():
                self[t] += 1
            else:
                self[t] = 1
    
    # Pairs a token to its relative frequency within the array
    def tf(self):
        total = sum(self.values())
        return { t : v/total for t, v in self.items()}

    # Pairs a token to its log normalized count
    def logNorm(self):
        return {t : log(1 + v) for t, v in self.items()}

    # Pairs a token to its double K-normalization value
    def dNorm(self, K):
        maxCount = max(self.values())
        return {t : K+(1-K)*(v/maxCount) for t, v in self.items()}

## Testing file
def testing():
    tokens = ['it', 'is', 'what', 'it', 'is']
    dV = Vectorize(tokens)
    print(f'Count Vector:\n\t{dV}\n')
    print(f'Term-Freq Vector:\n\t{dV.tf()}\n')
    print(f'Log-Norm Vector:\n\t{dV.logNorm()}\n')
    print(f'Double-Norm Vector (K = 0.5):\n\t{dV.dNorm(0.5)}\n')
