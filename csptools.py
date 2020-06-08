from relational_structure import *
from equations import *

def complexity(A):
    for s in siggers(A):
        return "P"
    
    return "NP-complete"