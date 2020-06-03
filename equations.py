from polymorphisms import homomorphisms
from itertools import product
from relational_structure import *
from csptosat import *
import partition
import logging

def polymorphismsWithIdentities(A,B,equations,idempotent=False):
    """ Each equation is of the form (args1, args2) where args1,args2 are tuples
        whose entries are single letter variables.
        Example: An equation (('xyx'),('yxx')) talks about a ternary function which
        satisfies
            forall x,y, f(x,y,x) = f(y,x,x).
        All these equations must have the same arity. """    
    
    logging.debug('polymorphismsWithIdentities:')
    
    # Checks
    # If no equation is given, add f(x)=f(x) as an equation.
    if len(equations) == 0:
        equations.append(('x','x'))

    # Check that all equations have the same arity
    arity = len(equations[0][0])
    for p in equations:
        if len(p[0]) != arity or len(p[1]) != arity:
            logging.error('equations::hasPolymorphism: LHS has {:d} and RHS has {:d} variables'.format(len(p[0]),len(p[1])))
            raise Exception
            
    An = A.power(arity)
    logging.debug('polymorphismsWithIdentities:Computed Power')
    indicatorPartition = partition.Partition(An.domain)
    logging.debug('polymorphismsWithIdentities:Computed Partition')
    for p in equations:
        variables = list(set(p[0]) | set(p[1]))
        for instanciations in product(A.domain, repeat=len(variables)):
            tuple1 = tuple( instanciations[variables.index(p[0][i])] for i in range(0,arity) )
            tuple2 = tuple( instanciations[variables.index(p[1][i])] for i in range(0,arity) )
            indicatorPartition.union(tuple1,tuple2)

    Factor = An.quotient(indicatorPartition)
    logging.debug('polymorphismsWithIdentities:Computed Factor Structure')
    L={}
    if idempotent==True and (set(A.domain) & set(B.domain) == set(A.domain)):
        for x in A.domain:
            representative = An.domain[indicatorPartition.representative(tuple(x for i in range(0,arity)))]
            L[representative] = {x}
            
    for a in product(A.domain,repeat=arity):
        representative = An.domain[indicatorPartition.representative(a)]
        if representative not in L:
            L[representative] = set(B.domain)
    logging.debug('polymorphismsWithIdentities:Finished preparing the factor')

    yield from homomorphisms(Factor,B,L)
    #return csptosat(Factor,B,L)

def siggers(A):
    Siggers = [ ('xyzx', 'yxyz') ]
    yield from polymorphismsWithIdentities(A,A,Siggers)
    
# check if A has a ternary WNU
def ternaryWNU(A):
    TernaryWNU = [ (('x','x','y'),('x','y','x')),
            (('x','x','y'),('y','x','x'))]
    yield from polymorphismsWithIdentities(A,A,TernaryWNU)
    
def ternaryQNU(A):
    TernaryQNU = [ ('xxy','xyx'),('xyx','yxx'),('yxx','xxx')]
    yield from polymorphismsWithIdentities(A,A,TernaryQNU)
    
def majority(A):
    majority = [ ('xxy','xyx'),('xyx','yxx'),('yxx','xxx')]
    yield from polymorphismsWithIdentities(A,A,majority,idempotent=True)

def malcev(A):
    Malcev = [ (('y','x','x'),('x','x','y')), (('y','x','x'),('y','y','y')) ]
    yield from polymorphismsWithIdentities(A,A,Malcev)

