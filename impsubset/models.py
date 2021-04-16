from functools import reduce
import itertools
from subsetInf import *

"""
class Model:

    # output is going to be a couter-model, input will be the same as what the user did for other class (engine)
    def __init__(self, lopt, engine):
        self.uni = engine.database.universe
        self.lopt = lopt
        lall = filter(lambda x: x[0] == "a", lopt)
        lall = map(lambda x: [x[1], x[2]], lall)
        self.all = set(reduce(lambda a, d: a + d, lall))
        lsome = filter(lambda x: x[0] == "i", lopt)  # M
        lsome = map(lambda x: [x[1], x[2]], lsome)
        self.some = set(reduce(lambda a, d: a + d, lsome))
        self.lon = engine.database.universe
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
        cprod = itertools.product(lon, repeat=2)
        state = set([])
        for pair in cprod:
            print(pair)
            v1, v2 = pair
            if (len(self.meaning[v1]) == 1) and ("non" in self.meaning[v2]):
                return True
            else:
                return False

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
        li = list(self.some)
        state = [li[0], li[len(li) - 1]]
        # case 1 all logic
        if t == 'a':
            ntarget = self.semanticn(self.engine.target)
            self.lopt.append(ntarget)
            print(self.engine.database.meaning)
            return self.sfinder(state, self.lon)
        # case 2
        else:
            return self.sfinder(state, self.some)

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

    def gencm(self):
        if not self.engine.gen_tf():
            print()
            print("We go on to generate a countermodel:")
            self.countermodel(self.lopt, self.engine.target)


class Modelarc(Model):
    def __init__(self, lopt, engine):
"""


# these are all assuming that our phi is a translated tag fact of the form ('a', 1, 0)
def semanticn(phi, universe):
    rt, rv1, rv2 = phi
    rv2 = N(rv2)
    rv2.negate(len(universe))  # put an actual n in here
    jrv2 = rv2.val
    if rt == 'a':
        rt = 'i'
    else:
        rt = 'a'
    return rt, rv1, rv2


def checkcon(loptf, universe):
    for tf in loptf:
        contrad = semanticn(tf, universe)
        if contrad in loptf:
            return tf, loptf
    return True


def echecker(lon, lopn, meaning, universe):
    for pair in itertools.product(lon, repeat=2):
        n1, n2 = pair
        nn2 = N(n2)
        nn2.negate(len(universe))
        if (n1, nn2.val) in lopn:
            return False
    return True


def sfinder(inputlist, lopn, lon, meaning, universe):
    ans = inputlist
    for noun in lon:
        ans.append(noun)
        extend = echecker(ans, lopn, meaning, universe)
        if extend:
            continue
        else:
            ans.remove(noun)
            nn = N(noun)
            nn.negate(len(universe))
            ans.append(nn.val)
    return ans


def mfinder(lopt, lopn, lon, meaning, universe):
    some = filter(lambda x: x[0] == "i", lopt)
    some = map(lambda x: [x[1], x[2]], some)
    for pair in some:
        if echecker(pair, lopn, meaning, universe):
            return sfinder(pair, lopn, lon, meaning, universe)


def countermodel(target, lopt, lopn, lon, meaning, universe):
    tt, tv1, tv2 = target
    if tt == "a":
        pass
    else:
        return mfinder(lopt, lopn, lon, meaning, universe)

