from csptools import *
from absorption import *

VH = {0,1}
EH = [ (0,1),(1,0) ]
P1 = RelationalStructure(VH, [[EH,2]])

n = None
for m in majority(P1):
    n = m
    break

absorbing = tuple( B for B in absorbingSubsets({0,1},n,3))
assert(absorbing == ({0},{1},{0,1}))

assert(isCenter({0,1},{0},n,3))

assert(isAbsorbingClone({0,1},{0},n,3,2) == False) # {0} does not binary absorb {0,1}
assert(isAbsorbingClone({0,1},{0},n,3,3) == True)
for R in essentialRelations({0,1},{0},n,3,2):
    assert(R == {(0,1),(1,0)})
for R in essentialRelations({0,1},{0},n,3,3):
    assert(False) # no ternary essential relation exists, since {0} ternary absorbs {0,1}