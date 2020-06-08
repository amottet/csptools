from itertools import product
import collections

def isAbsorbing(A,B,f,arity):
    for a,b in product(A, product(B,repeat=arity-1)):
        deque_b = collections.deque(b)
        deque_b.append(a)
        for i in range(arity):
            # check that f(b) is a subset of B
            if f[tuple(deque_b)] & B != f[tuple(deque_b)]:
                return False
            deque_b.rotate()
            
    return True

def absorbingSubsets(A,f,arity):
    list_A = list(A)
    for counter in range(1,2**(len(list_A))):
        B = { list_A[i] for i in range(len(list_A)) if counter & 2**i == 2**i }
        if isAbsorbing(A,B,f,arity):
            yield B