from itertools import *
import collections
import logging

def oneStepClosure(B,f,arity):
    """ Returns B union f(B,...,B). """
    result = B
    for b in product(B,repeat=arity):
        result.add(f[b])
    return result

def subuniverseGenerated(B,f,arity):
    """ Returns the closure of B in the clone generated by f. """
    result = set(B)
    length = 0
    while length < len(result):
        length = len(result)
        result = oneStepClosure(result,f,arity)
    return result

def isAbsorbing(A,B,f,arity):
    """ Returns True iff B absorbs A with respect to f. """
    for a,b in product(A, product(B,repeat=arity-1)):
        deque_b = collections.deque(b)
        deque_b.append(a)
        for i in range(arity):
            # check that f(b) is a subset of B
            if f[tuple(deque_b)] not in B:
                return False
            deque_b.rotate()
            
    return True

def essentialRelations(A,B,f,arity,essentialArity):
    """ Generates all the B-essential relations of given essentialArity in the algebra (A;f). """
    OneAInB = []
    productf = dict()
    for a in product(product(A,repeat=essentialArity), repeat=arity):
        productf[a] = tuple( f[ tuple( a[i][j] for i in range(arity) ) ] for j in range(essentialArity) )
    
    for b,a in product(product(B, repeat=essentialArity-1),A-B):
        deque_b = collections.deque(b)
        deque_b.append(a)
        OneAInB.append(tuple(deque_b))
    
    for s in combinations_with_replacement(OneAInB,essentialArity):
        deque_tuples = [ collections.deque(s[i]) for i in range(essentialArity) ]
        rotated_tuples=set()
        for i in range(essentialArity):
            deque_tuples[i].rotate(i)
            rotated_tuples.add(tuple(deque_tuples[i]))
        
        R = subuniverseGenerated(rotated_tuples,productf,arity)
        if R & set(product(B,repeat=essentialArity)) == set():
            yield R

def isAbsorbingClone(A,B,f,arity,arityOfAbsorption):
    """ Returns True iff B absorbs (A;f) by an operation of arity arityOfAbsorption. """
    for R in essentialRelations(A,B,f,arity,arityOfAbsorption):
        return False
    return True
        

def absorbingSubsets(A,f,arity):
    """ Generates all the absorbing subuniverses of the algebra (A;f). """
    list_A = list(A)
    for counter in range(1,2**(len(list_A))):
        B = { list_A[i] for i in range(len(list_A)) if counter & 2**i == 2**i }
        if isAbsorbing(A,B,f,arity):
            yield B
            
def isCenter(A,C,f,arity):
    """ Returns True iff C absorbs A with respect to f and C is a center of the algebra (A;f). """
    if not isAbsorbing(A,C,f,arity):
        return False
    
    f2 = dict()
    for a in product(A,repeat=arity):
        for a2 in product(A,repeat=arity):
            f2[tuple(zip(a,a2))] = (f[a],f[a2])
    
    for a in A-C:
        D = subuniverseGenerated(set(product(C,{a})) | set(product({a},C)),f2,arity)
        if (a,a) in D:
            return False
    return True