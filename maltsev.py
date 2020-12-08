from itertools import *
from solver import Solver
import general
import operation
import equations

class MaltsevSolver(Solver):
    def __init__(self,rel,maltsev=None):
        super().__init__(rel)
        self.m = operation.Operation(rel.domain,3)
                
        if maltsev == None:
            for m in equations.malcev(rel):
                maltsev = m
                break
        if maltsev == None:
            raise Exception
        else:
            self.m.defineFromMap(maltsev)
            
    # decides if { a in R | (a_{s[0]},...,a_{s[m-1]}) in S } is nonempty, and returns a tuple in this relation if it is the case
    def NonEmpty(self,reprR,s,S):
        U = set(reprR)
        prU = general.computeProjectionGeneral(U,s)
        oldlen = 0
        
        # Saturate U under the maltsev operation until its projection to coordinates (s[0],...,s[m-1]) stabilises
        # Takes time at most |A|^m
        while len(prU)>oldlen:
            oldlen = len(prU)
            for a,b,c in product(U,repeat=3):
                d = self.m.getValueTuple((a,b,c))
                projd = general.computeProjectionTuple(d,s)
                
                if projd in S:
                    return d
                if projd not in prU:
                    U.add(d)
                    prU.add(projd)
        
        return False

    # computes a compact representation of T = { a in R | aj = c}, assuming that R is already constant on (0,...,j-1)
    def FixValue(self,reprR,n,j,c):
        reprT = set()
        
        for i,a,b in product(range(n),self.template.domain,self.template.domain):
            wit1,wit2 = None,None
            
            # If i<=j the only possible forks in T have a=b
            if i <= j and a!=b:
                continue
            
            for u,v in product(reprR,reprR):
                if u[:i] == v[:i] and u[i]==a and v[i]==b:
                    wit1 = u
                    wit2 = v
                    
                    if a==b:
                        wit2 = wit1
                    break
            # If wit1 is still undefined, (i,a,b) is not even in Sig_R
            if wit1 == None:
                continue
            #print('Possible fork:',i,a,b)
            t1 = self.NonEmpty(reprR,(j,i),[(c,a)])
            #print(wit1)
            #print(wit2)
            #print(t1)
            if t1!=False:
                reprT.add(t1)
                reprT.add(self.m.getValueTuple((t1,wit1,wit2)))
        return reprT
        
    # computes a compact representation of { s in R | s1=t1,...,sm=tm }
    def FixValues(self,reprR,n,t):
        newRepr = reprR
        for j in range(len(t)):
            newRepr = self.FixValue(newRepr,n,j,t[j])
        return newRepr

    # computes a compact representation of { s in R | (s_{t1},...,s_{tm}) in S }
    def Next(self,reprR,n,t,S):
        reprT = set()
        
        for i,a,b in product(range(n),self.template.domain,self.template.domain):
            t1 = self.NonEmpty(reprR,t+(i,),productRelationsFlat(S,a))
            if not t1:
                continue
            restriction = self.FixValues(reprR,n,t1[:i])    
            t2 = self.NonEmpty(restriction,t+(i,),productRelationsFlat(S,b))
        
            
            if not t2:
                continue
            reprT.add(t1)
            reprT.add(t2)
        return reprT
    
    def solve(self,X):
        n = len(X.domain)
        R = representationFullRelation(self.template.domain, n)
        for i in range(len(X.relations)):
            SX = X.relations[i]
            SA = self.template.relations[i]
            for a in SX:
                R = self.Next(R,n,a,SA)
                if len(R) == 0:
                    return None
        h = None
        for sol in R:
            h = sol
            break
        return h
    
def productRelationsFlat(R,a):
    result = set()
    for t in R:
        newlist = list(t)
        newlist.append(a)
        result.add(tuple(newlist))
    return result

# computes a compact representation of R
def computeRepresentation(A,R,n):
        reprR = []
        for (i,a,b) in product(range(n),A,A):
            for t,t2 in product(R,R):
                if t[:i]!=t2[:i] or t[i] != a or t2[i] != b:
                    break
                        
                reprR.append(t)
                reprR.append(t2)
        return reprR
    
# computes a compact representation of A^n
def representationFullRelation(A,n):
    d = None
    representation = set()

    for d2 in A:
        d = d2
        break
    ed = [ d for i in range(n) ]
    for i in range(n):
        for a in A:
            ea = list(ed)
            ea[i] = a
            representation.add(tuple(ea))

    return representation