import syllogistic
from subsetInf import *


def checkhelp(p, nons):
    for n in nons:
        if p <= n:
            return True
    return False


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
        t, v1, v2 = phi
        rt, rv1, rv2 = phi
        rv2 = N(v2)
        rv2.negate(len(self.uni))  # put an actual n in here
        if t == 'a':
            rt = 'i'
        else:
            rt = 'a'
        return rt, rv1, rv2

    def echecker(self):
        # return boolean
        nons = [x for x in self.meaning if "non" in self.meaning[x]]
        pos = [x for x in self.meaning if x not in nons]

        return any(map(lambda x: checkhelp(x, nons), pos))

    def sfinder(self):
        inp = self.lon
        idx = len(self.meaning)
        if self.echecker():
            for noun in self.lon:
                nounval = self.meaning[noun]
                negval = N(noun)
                negval.negate(len(self.uni))
                self.meaning[idx] = noun
                if not self.echecker():
                    del self.meaning[idx]
                else:
                    idx += 1
                self.meaning[idx] = negval
                if not self.echecker():
                    del self.meaning[idx]
                else:
                    idx += 1
        return inp

    def countermodel(self):
        t = self.engine.target[0]
        provables = syllogistic.provables([], [])  # L
        if t == 'a':
            ntarget = self.semanticn(self.engine.target)
            provables.append(ntarget)
            all = filter(lambda x: x[0] == "a", provables)
            # case 1 all logic

        else:
            some = filter(lambda x: x[0] == "i", provables)  # M
            # case 2
            state = self.sfinder()

    def checkcon(self, lot):
        verbs = []
        raw_vars = set()
        provables = syllogistic.provables(verbs, raw_vars)
        # do list comprehension
        for phi in lot:
            nphi = self.semanticn(phi)
            if nphi in lot:
                return True
        else:
            return False
