import copy
import itertools

class Operation:
    def __init__(self,domain,arity):
        self.domain = domain
        self.arity = arity
        self.table = dict()

    # no check whatsoever
    def define(self,argument,value):
        self.table[argument] = value
        
    def defineFromMap(self,definingList):
        self.table = copy.deepcopy(definingList)
        
    def getValue(self,argument):
        return self.table[argument]
    
    def getArity(self):
        return self.arity
    
    def getDomain(self):
        return self.domain
    
    # expects argument to be a tuple (of length the arity of the operation) of tuples, all of the same length
    # the operation is applied componentwise
    def getValueTuple(self,argument):
        power = len(argument[0])
        return tuple( self.getValue(tuple(argument[j][i] for j in range(self.arity))) for i in range(power) )
 