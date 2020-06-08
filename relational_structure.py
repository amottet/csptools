from itertools import product
from partition import *

class NonCompatibleStructures(Exception):
    pass

class InvalidRelation(Exception):
    pass

# Checks that all tuples in R have length k
def checkRelationArity(k,R):
    for t in R:
        if len(t) != k:
            raise InvalidRelation

def checkRelationDomain(domain,R):
    for a in R:
        for i in range(len(a)):
            if a[i] not in domain:
                raise InvalidRelation


class RelationalStructure:
    def __init__(self, S, rels):
        self.domain = list(S)
        self.relations = []
        self.arities = []
        for [R, k] in rels:
            checkRelationArity(k,R)
            checkRelationDomain(self.domain,R)
            self.relations.append(list(R))
            self.arities.append(k)

    def type(self):
        return self.arities
    
    def domain(self):
        return set(self.domain)

    def power(self,k):
        rels2 = []
        domain2 = product(self.domain, repeat=k)
        for i in range(0,len(self.relations)):
            R = []
            for perm in product(self.relations[i], repeat=k):
                new_tuple = tuple( tuple( perm[l][j] for l in range(0,k)) for j in range(0,self.arities[i])) 
                R.append(new_tuple)
            rels2.append([R,self.arities[i]])
        return RelationalStructure(domain2,rels2)

    def product(self, B):
        if(self.type() != B.type()):
            raise NonCompatibleStructures

        rels2 = []
        domain2 = product(self.domain,B.domain)
        for i in range(0,len(self.relations)):
            R = [ list(zip(s,t)) for s in self.relations[i] for t in B.relations[i] ]
            rels2.append([R, self.arities[i]])
        return RelationalStructure(domain2, rels2)

    def quotient(self,Theta):
        domain2 = Theta.blocks()
        rels2 = []
        for i in range(0,len(self.relations)):
            R = set()
            for t in self.relations[i]:
                s = tuple( self.domain[Theta.representative(t[j])] for j in range(0,self.arities[i]) )
                R |= {s}
            rels2.append( (R,self.arities[i]) )
        return RelationalStructure(domain2,rels2)
        
                
    def __or__(self, t):
        if len(t)!=2:
            return self

        rels2 = []
        for i in range(0,len(self.relations)):
            rels2.append([self.relations[i], self.arities[i]])
        rels2.append(t)
        return RelationalStructure(self.domain, rels2)