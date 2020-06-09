from solver import *
from relational_structure import *
import logging

Domain = {1,2,3}
E = [ [1,2],[2,3],[2,1],[3,2],[1,3],[3,1]]
K3 = RelationalStructure(Domain, [[E,2]])

try:
    solver = ZhukSolver(K3)
    assert(False) # K3 has no Taylor polymorphism, which should be detected by the solver
except:
    pass

VP2d = {'a','b','c'}
EP2d = [ ('a','b'), ('b','c') ]
P2d = RelationalStructure(VP2d, [[EP2d,2]])
VH = {0,1}
EH = [ (0,1),(1,0) ]
P1 = RelationalStructure(VH, [[EH,2]])
P1d = RelationalStructure({'s','t'}, [[[('s','t')],2] ])

logging.getLogger().setLevel(logging.INFO)
solver = ZhukSolver(P2d)
assert(solver.poly != None)
assert(solver.solve(P1) == None)
print(solver.absorbingSubuniverses)
print(solver.centers)

ac = ACSolver(P2d)
assert(ac.solve(P1) == None)
assert(ac.solve(P1d) != None)

sat = SATSolver(P2d)
assert(sat.solve(P1) == None)
assert(sat.solve(P1d) != None)
