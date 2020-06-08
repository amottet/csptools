from relational_structure import *
from consistency import *
from absorption import *
from equations import *


# Testing projections
R = [ (1,2,3), (2,1,3), (3,1,2) ]
proj = computeProjectionGeneral(R, (0,1))
assert(proj == { (1,2), (2,1), (3,1) })

proj = computeProjectionGeneral(R, (1,2))
assert(proj == { (1,3), (2,3), (1,2) })

proj = computeProjectionGeneral(R, (2,0))
assert(proj == { (3,1), (3,2), (2,3) })

proj = computeProjectionGeneral(R, (2,2,0))
assert(proj == { (3,3,1), (3,3,2), (2,2,3) })


# Checking arc consistency
VK3 = {1,2,3}
EK3 = [ (1,2),(2,1),(1,3),(3,1),(2,3),(3,2) ]
K3 = RelationalStructure(VK3, [[EK3,2]])

VH = {0,1}
EH = [ (0,1),(1,0) ]
P1 = RelationalStructure(VH, [[EH,2]])
P1d = RelationalStructure({'s','t'}, [[[('s','t')],2] ])

VP2d = {'a','b','c'}
EP2d = [ ('a','b'), ('b','c') ]
P2d = RelationalStructure(VP2d, [[EP2d,2]])

L=dict()
L[0]=set(VP2d)
L[1]=set(VP2d)
S = computeIntersection(EP2d,L,[0,1])
arcReduce(S,L,[0,1])
assert(L[0] == {'a','b'})
assert(L[1] == {'b','c'})
T = computeIntersection(EP2d,L,[1,0])
assert(arcReduce(T,L,[1,0]) == None)


L = arcConsistency(K3,P1)
assert(L[1] == {0,1})
assert(L[2] == {0,1})
assert(L[3] == {1,0})

L = arcConsistency(P1,K3)
assert(L[0] == {1,2,3})
assert(L[1] == {1,2,3})

L2 = ac3(P1d,P2d)
assert(L2['s'] == {'a','b'})
assert(L2['t'] == {'b','c'})

assert(arcConsistency(P1,P2d) == None)
