from pysat.solvers import Glucose3
from relational_structure import *
from itertools import *
from consistency import computeIntersection,arcConsistency,ac3
import logging

class SatThread:
    def __init__(self,A,B,L,table,range_of_relations):
        self.A = A
        self.B = B
        self.L = L
        self.table = table
        self.clauses = []
        
    def run(self):
        pass
        
        
# The argument L specifies for each a in A, a set of elements of B that contains the possible values for a
# The argument extentRelations specifies for each constraint (a1,...,ak) in A,
# a k-ary relation of B that gives the possible values for the constraint
def buildSATInstance(g,A,B,L,extentRelations):
    # We have 2 types of variables:
    # x_a,b means a is mapped to b                                              (primary variable)
    # y_t,b1,...,bk means t is mapped to b1,...,bk                              (secondary variable)
    # We have 4 types of constraints:
    # 1) For all a: \/_b x_a,b where the disjunction runs through b in L[a]     "a is mapped to at least one of the elements in L[a]"
    # 2) For all a and b\neq b': not x_a,b \/ not x_a,b'                        "a is not mapped to two different elements"
    # 3) For all k-tuples t in A: \/_b1,...,bk y_t,b1,...,bk where the disjunctions runs through (b1,...,bk) in extentRelations[t]
    # 4) y_t,b1,...,bk -> x_t[i],bi
    if A.type() != B.type():
        raise NonCompatibleStructures

    # Maps elements of the CSP instance to id of variable in the resulting CNF formula.
    # Is used for the construction of the instance, but can be discarded after.
    table = {}
    
    # Maps id of variable to element of instance.
    # We only care about the variables of the first type (primary variables).
    # Is used to decode the model.
    reverseTable = []
    
    nbvars = 0
    cntPrimaryVariables = 0
    clauses = []
    for a in A.domain:
        for b in L[a]:
            nbvars+=1
            table[(a,b)] = nbvars
            reverseTable.append((a,b))
    cntPrimaryVariables = nbvars
            
    for k in range(len(A.relations)):
        R = A.relations[k]
        
        for a in R:
            S = extentRelations[tuple(a)]
            for b in S:
                nbvars+=1
                table[(tuple(a),tuple(b))] = nbvars
                
    for a in A.domain:
        g.add_clause([table[(a,b)] for b in L[a] ]) # 1
        #print([table[(a,b)] for b in B.domain ])
        for b1,b2 in product(L[a],repeat=2):
            if b1 != b2:
                g.add_clause([ -table[(a,b1)],-table[(a,b2)] ]) #2
                #print([-table[(a,b1)],-table[(a,b2)]])
    
    
    for k in range(len(A.relations)):
        RA = A.relations[k]
                
        for a in RA:
            S = extentRelations[tuple(a)]
            g.add_clause( [ table[(tuple(a),tuple(b))] for b in S ]) #3
            for b in S:
                for j in range(len(a)):
                    #print(a,b,j,[-table[(tuple(a),tuple(b))], table[(a[j],b[j])]])
                    g.add_clause([-table[(tuple(a),tuple(b))], table[(a[j],b[j])]]) #4
        
    return (cntPrimaryVariables,reverseTable)

def csptosat(A,B,initialL=None):
    L,newSignature = ac3(A,B,initialL,None,True)
    
    if L == None:
        return None
 
    logging.debug('csptosat:Starting glucose')
    g = Glucose3()
    cntPrimaryVariables,table = buildSATInstance(g,A,B,L,newSignature)
    logging.debug('csptosat:instance built, {:d} variables'.format(cntPrimaryVariables))
    if g.solve():
        logging.debug('csptosat:solved')
        sol = g.get_model()
        h = {}
        for i in range(cntPrimaryVariables):
            if sol[i]>0:
                (a,b) = table[i]
                h[a]=b
        g.delete()
                    
    else:
        h = None
    g.delete()
    return h

def outputdimacs(A,B,initialL=None):
    """ Outputs the SAT instance for the homomorphism problem A->B? in the DIMACS format, widely accepted as standard format for SAT solvers. """
    """ The output is written in the file cnf.tmp """
    L = ac3(A,B,initialL)
    
    if L == None:
        return None
    
    instance = buildSATInstance(A,B,L)

    output = open('cnf.tmp','w')
    output.write('p cnf {:d} {:d}\n'.format(instance[0],len(instance[1])))
    for c in instance[1]:
        for l in c:
            output.write('{:d} '.format(l))
        output.write('0\n')