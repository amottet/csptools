from csptools import *
import logging

logging.getLogger().setLevel(logging.INFO)

domain = {1,2,3}
E = [ [1,2],[2,3] ] # list of pairs...
F = [ [3,1], [1,3] ]
structure = RelationalStructure(domain, [[E,2], [F,2]])

# outputs a majority polymorphism
for m in majority(structure):
    print(m)
    break
    
for o in olsak(structure,structure):
    print(o)
    break
