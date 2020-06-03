from relational_structure import *
from polymorphisms import *
from equations import *

def complexity(A):
    for s in siggers(A):
        return "P"
    else:
        return "NP-complete"