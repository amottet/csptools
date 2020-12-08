from itertools import *
import consistency
import operation
from relational_structure import *
from maltsev import *

op = dict()
for a,b,c in product({0,1},repeat=3):
    op[(a,b,c)] = (a+b+c)%2
G0 = [ (a,b,c) for a,b,c in product({0,1},repeat=3) if (a+b+c)%2==0 ]
G1 = [ (a,b,c) for a,b,c in product({0,1},repeat=3) if (a+b+c)%2==1 ]
Str = RelationalStructure({0,1}, [[G0,3],[G1,3]])

solver = MaltsevSolver(Str)
G0X = [(1,2,3)]
G1X = [(0,1,2),(0,2,3)]
X = RelationalStructure({ i for i in range(10)}, [[G0X,3],[G1X,3]])
print(solver.solve(X))

Horn = [(0,0,0),(0,1,0),(1,0,0),(0,0,1),(0,1,1),(1,0,1),(1,1,1)]
try:
    MaltsevSolver(RelationalStructure({0,1},[[Horn,3]]))
    assert(False) # Horn SAT has no Maltsev term, this should be detected while constructing the solver
except Exception:
    pass