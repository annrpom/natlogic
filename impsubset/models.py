from functools import reduce
import itertools
import syllogistic
from subsetInf import *


class Model:

    # output is going to be a couter-model, input will be the same as what the user did for other class (engine)
    def __init__(self, set, lon, engine):
        self.uni = set
        self.lon = lon
        self.engine = engine
        self.meaning = engine.database.meaning
        # notes: wanna gen everything that has compliment in them, generate all provable ones
        # if contrad, break
        # orthoposet
        # some x are y -> x and y both state

    # these are all assuming that our phi is a translated tag fact of the form ('a', 1, 0)
    def semanticn(self, phi):
        rt, rv1, rv2 = phi
        rv2 = N(rv2)
        rv2.negate(len(self.uni))  # put an actual n in here
        rv2 = rv2.val
        if rt == 'a':
            rt = 'i'
        else:
            rt = 'a'
        return rt, rv1, rv2

    def echecker(self, lon):  # lop is a list of pairs
        # return boolean
        # all x are non-y counts, does all non-x are non-y count
        cprod = itertools.product(lon)
        state = set([])
        for pair in cprod:
            v1, v2 = pair
            if (len(self.meaning[v1]) == 1) and ("non" in self.meaning[v2]):
                return False
            else:
                state.add(v1)
                state.add(v2)
        return state

    # all we are doing now is finding states (think orthoposet)
    def sfinder(self, inputl, lon):
        state = self.echecker(inputl)  # input list is extendable
        for x in lon:
            state.add(x)
            if self.echecker(state):
                continue
            else:
                state.remove(x)
                nx = N(x)
                nx.negate(len(self.uni))
                state.add(nx.val)
        return state

    def countermodel(self, lopt, target):
        t = target[0]
        # case 1 all logic
        if t == 'a':
            all = filter(lambda x: x[0] == "a", lopt)
            all = map(lambda x: [x[1], x[2]], all)
            lon = set(reduce(lambda a, d: a + d, all))
            ntarget = self.semanticn(self.engine.target)
        # case 2
        else:
            some = filter(lambda x: x[0] == "i", lopt)  # M
            some = map(lambda x: [x[1], x[2]], some)
            losomen = set(reduce(lambda a, d: a + d, some))
            if self.echecker(losomen):
                return self.sfinder(losomen, self.lon)
            else:
                print("ask what to do here")

    # going to assume we get provables as input
    def checkcon(self, lopt):
        # do list comprehension
        for phi in lopt:
            nphi = self.semanticn(phi)
            if nphi in lopt:
                # so i do not have to look up the thing that makes it consistent or not
                return phi, nphi
        else:
            return True
