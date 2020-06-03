import consistency
import general
import logging
import itertools


def printPoly(domain,f,arity):
    for a in itertools.product(domain,repeat=arity):
        print(a,f[a])


# key is a tuple of size m, pattern is a tuple of size n whose elements are in {0,...,m-1}
def expand(key,pattern):
    return tuple( key[pattern[i]] for i in range(len(pattern)) )

# Takes an operation f of arity arityOfMinor and produces a function g of arity arityOfFunction such that f is the minor of g according to the pattern.
# The function g might already be partially defined, if some value is conflicting then the function returns False.
# Example: For arities 3,4 and pattern [0,1,0,2] we obtain a partial g defined by g(x,y,x,z)=f(x,y,z)
def expandMinor(A,B,minor,arityOfMinor,function,arityOfFunction,pattern):
    for a in itertools.product(A.domain, repeat=arityOfMinor):
        b = expand(a, pattern)
        if b in function:
            if function[b]!=minor[a]:
                function = {}
                return False
        else:
            function[b] = minor[a]
    return True

# Takes an operation g of arity arityOfFunction and produces a function f of arity arityOfMinor such that f is the minor of g according to the pattern.
# Example: For arities 3,4 and pattern [0,0,1,2] we obtain f(x,y,z)=g(x,x,y,z)
def collapseMinor(A,B,minor,arityOfMinor,function,arityOfFunction,pattern):
    for a in itertools.product(A.domain, repeat=arityOfMinor):
        b = expand(a, pattern)
        if b in function:
            minor[a] = function[b]

# For every input for which f is not defined, define the value at that input to be the codomain of the function.
def finalizeFunction(A,B,f, arity):
    for a in itertools.product(A.domain, repeat=arity):
        if a not in f:
            f[a] = B.domain
            
                
# generates all possible extensions of the partial function f within the set S
def extensions(G,f,S,arity):
    for candidateExtension in S:
        extends = True
        for a in itertools.product(G.domain,repeat=arity):
            if a in f and candidateExtension[a]!= f[a]:
                extends=False
                break
        if extends == True:
            yield candidateExtension
            
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
            
            
# yields the polymorphisms of arity n assuming the polymorphisms of arity n-1 are known and stored in file with name s
def polymorphismsFromMinors(A,B,n,s):
    cnt = 0
    polys = general.loadFromFile(s)
    print("Loaded " + str(len(polys)) + " polymorphisms of arity " + str(n-1))
    An = A.power(n)
    
    pattern1 = [0] # [0 0 1 ... n - 2] i.e. f(x x y z t...)
    for i in range(n-1):
        pattern1.append(i)
    
    for f in polys:
        partial = {}
        # partial(x1,x1,...,xn-1) := f(x1,...,xn-1)
        expandMinor(A,B,f,n-1,partial,n,pattern1)
        finalizeFunction(A,B,partial,n)
        yield from homomorphisms(An,B,partial)
        