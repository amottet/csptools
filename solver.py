import equations
import consistency
from csptosat import csptosat
import logging

class IntractableTemplate(Exception):
    pass

class Solver:
    def __init__(self,rel):
        self.template = rel
        
    def solve(self,X):
        raise NotImplementedError()
        

class ACSolver(Solver):
    def __init__(self,rel):
        super().__init__(rel)
    
    def solve(self,X):
        for h in homomorphisms(X,self.template):
            return h
        return None
    
class SATSolver(Solver):
    def solve(self,X):
        return csptosat(X,self.template)
    
# we assume the template is a core here
class ZhukSolver(Solver):
    def __init__(self,rel,wnu=None):
        super().__init__(rel)
        
        self.poly = None
        if wnu != None:
            self.poly = wnu
        else:
            for s in equations.siggers(self.template,idempotent=True):
                logging.info('ZhukSolver:Found a Siggers polymorphism of the template')
                self.poly = s
                break
            if self.poly == None:
                logging.info('ZhukSolver:The template has no idempotent Siggers polymorphism.')
                raise IntractableTemplate
                
    def solve(self,X):
        return None
    
    
    
# generates all homomorphisms from A to B that are compatible with the given initial data
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
        unpackedL = dict()
        for a in A.domain:
            for im in L[a]:
                unpackedL[a] = im
                break
        yield unpackedL
        
    else:
        oldSet = L[a]
        for b in oldSet:
            L[a] = {b}
            yield from homomorphisms(A,B,L)