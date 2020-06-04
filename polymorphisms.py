import consistency
import general
import logging
import itertools


def printPoly(domain,f,arity):
    for a in itertools.product(domain,repeat=arity):
        print(a,f[a])
            
# generates all homomorphisms from A to B that are compatible with the initial list
def homomorphisms(A,B, initialL=None):
    L = consistency.arcConsistency(A,B,initialL)
    
    if L == None:
        logging.info('homomorphisms:No homomorphism')
        return None
    
    # Finds the next element for which the homomorphism value is not uniquely defined
    nextElem = None
    for a in A.domain:
        if len(L[a])>1:
            nextElem = a
            break

    # If no such element exists, the homomorphism is completely defined and we return it
    if nextElem == None:
        yield L
        
    else:
        oldSet = L[a]
        for b in oldSet:
            L[a] = {b}
            yield from homomorphisms(A,B,L)