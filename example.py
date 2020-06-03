from csptools import *

domain = {1,2,3}
E = [ [1,2], [2,3] ] # list of pairs...
F = [ [3,1], [1,3] ]
structure = RelationalStructure(domain, [[E,2], [F,2]])

for m in majority(structure):
    print(m)
    break