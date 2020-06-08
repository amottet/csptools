from itertools import *
import collections
import logging

def oneStepClosure(B,f,arity):
    result = B
    for b in product(B,repeat=arity):
        result.add(f[b])
    return result

def subuniverseGenerated(B,f,arity):
    result = set(B)
    length = 0
    while length < len(result):
        length = len(result)
        result = oneStepClosure(result,f,arity)
    return result

def isAbsorbing(A,B,f,arity):
    for a,b in product(A, product(B,repeat=arity-1)):
        deque_b = collections.deque(b)
        deque_b.append(a)
        for i in range(arity):
            # check that f(b) is a subset of B
            if f[tuple(deque_b)] not in B:
                return False
            deque_b.rotate()
            
    return True

def absorbingSubsets(A,f,arity):
    list_A = list(A)
    for counter in range(1,2**(len(list_A))):
        B = { list_A[i] for i in range(len(list_A)) if counter & 2**i == 2**i }
        if isAbsorbing(A,B,f,arity):
            yield B
            
def isCenter(A,C,f,arity):
    f2 = dict()
    
    for a in product(A,repeat=3):
        for a2 in product(A,repeat=3):
            f2[tuple(zip(a,a2))] = (f[a],f[a2])
    
    for a in A-C:
        D = subuniverseGenerated(product(C|{a}, repeat=2),f2,arity)
        if (a,a) in D:
            return False
    return True