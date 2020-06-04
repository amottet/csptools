from itertools import product
import logging

def generatePartitions(size):
    """ Enumerate all the partitions of {0,...,size-1}
    in the form of a list L of lists.
    Each list L[i] contains a list of the integers in the i-th block of the partition. """
    if size == 1:
        yield [ [0] ]
    elif size > 1:
        for T in generatePartitions(size-1):
            yield T+[ [size-1] ]

            for i,part in enumerate(T):
                yield T[:i] + [[size-1]+part] + T[i+1:]

                    
class Partition:
    """ A partition of a set.

    Members are:
    - domain: the domain of the partition.
    - p: internal representation of the partition.
    """
    def __init__(self, S):
        # we use self.domain.index for the internal representation
        # so we need to handle the domain as a list
        self.domain = list(S)
        self.p = []
        for i in range(0,len(S)):
            self.p.append(i)

    def representative(self,a):
        """ Finds the position of the representative of a in p.

        :param a A member of self.domain.
        :return An integer in range(0,len(self.domain)).
            We have a/Theta = b/Theta iff Theta.representative(a)==Theta.representative(b).
        """
        if a not in self.domain:
            logging.error('The argument is not an element of',self.domain,a)
        else:
            i = self.domain.index(a)
            while i != self.p[i]:
                j = self.p[i]
                self.p[i] = self.p[self.p[i]]
                i = j
            return i
        
    def initializeWithBlocks(self,S,L):
        """ Initializes the partition from the list of blocks. """
        self.domain = list(S)
        self.p = []
        for i in range(0,len(S)):
            self.p.append(i)
        for B in L:
            first = B[0]
            for a in B:
                self.union(self.domain[a],self.domain[first])


    def union(self,a,b):
        """ Makes the union of the blocks of the partition
        that contain a and b.

        :param a A member of self.domain
        :param b A member of self.domain
        :return True iff a and b weren't already in the same block.
        """
        if a not in self.domain or b not in self.domain:
            logging.error('One of the two arguments does not belong to',self.domain)
        elif self.representative(a) == self.representative(b):
            return False
        else:
            self.p[self.representative(a)] = self.representative(b)
            return True

    def blocks(self):
        """ Returns a set containing the blocks of the partition. """
        B = []
        for a in self.domain:
            B.append(self.representative(a))
        return { self.domain[i] for i in B }

    def __iter__(self):
        self.iterprod = product(self.domain, repeat=2)
        return self

    def __next__(self):
        [a,b] = next(self.iterprod)
        while self.representative(a) != self.representative(b):
            [a,b] = next(self.iterprod)
        return [a,b]

    def intersection(self,Q):
        """ Finds the inf of self and Q. """
        if self.domain != Q.domain:
            logging.error('Partition::intersection: The two partitions must have the same domain.')
            return Partition(self.domain)
        R = Partition(self.domain)
        for a,b in self:
            if Q.representative(a) == Q.representative(b):
                R.union(a,b)
        return R

    def sup(self,Q):
        """ Finds the sup of self and Q."""
        if self.domain != Q.domain:
            logging.error('Partition::intersection: The two partitions must have the same domain.')
            return Partition(self.domain)
        R = Partition(self.domain)
        changed = 1
        while changed == 1:
            changed = 0
            for a,b in self:
                for c in self.domain:
                    if Q.representative(b)==Q.representative(c):
                        changed = changed or R.union(a,c)

            for a,b in Q:
                for c in self.domain:
                    if self.representative(b)==self.representative(c):
                        changed = changed or R.union(a,c)
        return R

    def print(self):
        L = [[] for i in range(0,len(self.domain))]
        for a in self.domain:
            L[self.representative(a)] = L[self.representative(a)] + [a]
        for B in L:
            if len(B)>0:
                print(B,end='')
        print()

