from csptools import *
from absorption import *

VH = {0,1}
EH = [ (0,1),(1,0) ]
P1 = RelationalStructure(VH, [[EH,2]])
P1d = RelationalStructure({'s','t'}, [[[('s','t')],2] ])

VP2d = {'a','b','c'}
EP2d = [ ('a','b'), ('b','c') ]
P2d = RelationalStructure(VP2d, [[EP2d,2]])

n = None
for m in majority(P1):
    n = m
    break

absorbing = tuple( B for B in absorbingSubsets({0,1},n,3))
assert(absorbing == ({0},{1},{0,1}))