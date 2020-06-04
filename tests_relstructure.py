from relational_structure import *
from itertools import *
from equations import *
import logging

Domain = {1,2,3}

E = [ [1,2], [2,3] ]
G = RelationalStructure(Domain, [[E,2]])
H = G.product(G)

assert(G.type() == [2])
assert(H.type() == [2])
assert(set(H.domain) == { (1,1), (2,2), (3,3), (1,3), (1,2), (3,1), (3,2), (2,3), (2,1) })
assert(H.relations[0] == [ [(1,1), (2,2)], [(1,2), (2,3)], [(2,1),(3,2)], [(2,2),(3,3)]] )

E = [ [1,2],[2,3],[2,1],[3,2],[1,3],[3,1]]
K3 = RelationalStructure(Domain, [[E,2]])
H = K3.power(4)
assert(H.domain == list(product({1,2,3},repeat=4)))
Theta = Partition(H.domain)
Theta.union( (1,1,1,1), (1,1,1,2) )
G = H.quotient(Theta)
assert(len(G.domain) == 3**4 - 1)

for [i,j,k] in product(Domain,repeat=3):
    Theta.union((i,i,i,i),(i,i,j,k))

assert(len(Theta.blocks()) == 6*9 + 3)
G = H.quotient(Theta)
assert(len(G.domain) == 6*9+3)