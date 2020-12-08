from relational_structure import *
import logging
import copy
import general

# Computes the composition of two binary relations
def computeComposition(R,S):
    result = set()
    for r,s in product(R,S):
        if r[1]==s[0]:
            result = result.add((r[0],s[1]))
    return result

# Returns the intersection of R with the product L[scope[0]]x...xL[scope[k-1]].
def computeIntersection(R,L,scope):
    S = []
    if len(R)==0:
        return []
    k = len(scope)
    
    for s in R:
        inside = True
        try:
            for i in range(0,k):
                if s[i] not in L[scope[i]]:
                    inside = False
                    break
        except:
            logging.critical('Relation =',R)
            logging.critical('Scope =',scope)
            logging.critical('Tuple in R =',s)
            logging.critical(i,k)
            logging.critical(L[scope[i]])
            exit()
            
        if inside:
            S.append(s)
    return S

# Projects R onto each of its coordinates and updates the lists L in the process.
# Returns True if some variable in scope has had its L-list changed and all lists are nonempty, False if no variable has changed,
# and None if some variable's list becomes empty.
def arcReduce(R,L,scope):
    if len(R) == 0:
        return None
    k = len(R[0])
    changed = False
    # Project the intersection on each coordinate
    for i in range(k):
        previousSize = len(L[scope[i]])
        L[scope[i]] = general.computeProjection(R,i)
        if previousSize > len(L[scope[i]]):
            changed = True
        
    return changed
       
def arcConsistency(A,B,initialL=None):
    """ Check whether there exists a homomorphism from A to B.
    :param A,B two structures of the same signature
    :param initialL A dictionary. 
            The key a of the dictionary contains a set S of elements from B.domain
            such that a is necessarily mapped to S.
    """
    if A.type()!=B.type():
        raise NonCompatibleStructures

    # We COPY the dictionary given in parameter to avoid side effects
    if initialL is None:
        L = {}
        for a in A.domain:
            if a not in L:
                L[a] = set(B.domain)
    else:
        L = dict(initialL)

    cntIterations = 0
    changed = True
    while changed == True:
        changed = False
        # For every relation of A:
        for i in range(len(A.relations)):
            RA = A.relations[i]
            RB = B.relations[i]      
            # For every tuple t of RA, we look for the tuples of RB that are compatible with L
            for t in RA:
                S = computeIntersection(RB,L,t)
                reductionResult = arcReduce(S,L,t)
                if reductionResult==None:
                    return None
                changed = changed | reductionResult
                cntIterations+=1
    #logging.info('Number of iterations of AC:', cntIterations)
    
    return L


def ac3(A,B,initialL=None,initialSignature=None,useExtentRelations=False):    
    if A.type()!=B.type():
        raise NonCompatibleStructures
    
    logging.debug('ac3:')
    # We COPY the dictionary given in parameter to avoid side effects
    
    if initialL is None:
        L = {}
        for a in A.domain:
            L[a] = B.domain
    else:
        L = dict(initialL)
    logging.debug('ac3:Finished preparing the L list')

    worklist = set()
    
    if useExtentRelations:
        if initialSignature is None:
            newSignature = {}

            for i in range(len(A.relations)):
                for a in A.relations[i]:
                    newSignature[tuple(a)] = B.relations[i]
        else:
            newSignature = dict(initialSignature)
                
    initialSizes = [ len(L[a]) for a in A.domain]
    
    for i in range(len(A.relations)):
        for a in A.relations[i]:
            worklist.add((tuple(a),i))
    
            
    # Builds an adjacency list:
    #for every a in the domain, adjacency[a] is a list of all (b,i) such that b is a tuple in A.relations[i] and a appears in b
    adjacency = {}
    for a in A.domain:
        adjacency[a] = set()
        for i in range(len(A.relations)):
            for b in A.relations[i]:
                if a in b:
                    adjacency[a].add((tuple(b),i))
            
    
    
    cntIterations = 0
    while len(worklist)>0:
        (a,i) = worklist.pop()
        previousLengths = [ len(L[a[j]]) for j in range(len(a)) ]
        
        if useExtentRelations:
            newSignature[a] = computeIntersection(newSignature[a],L,a)
            changed = arcReduce(newSignature[a],L,a)
        else:
            RB = B.relations[i]
            S = computeIntersection(RB,L,a)
            changed = arcReduce(S,L,a)
            
        if changed==None:
            if useExtentRelations:
                return None,None
            else:
                return None
        
        changedElements = [ a[j] for j in range(len(a)) if len(L[a[j]]) < previousLengths[j] ]
        for b in changedElements:
            worklist |= adjacency[b]
        cntIterations+=1
    #logging.info('Number of iterations of AC3:',cntIterations)
    
    if useExtentRelations:
        return L,newSignature
    else:
        return L