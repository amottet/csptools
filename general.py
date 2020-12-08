import pickle
import itertools

def saveToFile(L,s):
    with open(s,'wb') as filehandle:
        pickle.dump(L,filehandle)

def loadFromFile(s):
    filehandle = open(s, 'rb')
    return pickle.load(filehandle)

def constructProductFunction(domain,power,f,arity):
    productf = dict()
    for a in itertools.product(itertools.product(domain,repeat=power), repeat=arity):
        productf[a] = tuple( f[ tuple( a[i][j] for i in range(arity) ) ] for j in range(power) )
    return productf

def computeProjection(R,i):
    proj = { t[i] for t in R }
    return proj

# s is a tuple of entries from {0,...,arity(R)-1}.
# Returns the relation consisting of the tuples (t[s[0]],...,t[s[...]]) where t is in R.
def computeProjectionGeneral(R,s):
    k = len(s)
    proj = { tuple(t[s[i]] for i in range(k)) for t in R }
    return proj

# s is a tuple of entries from {0,...,ar(t)-1}
def computeProjectionTuple(d,s):
    return tuple(d[s[i]] for i in range(len(s)))