import syllogistic
from subsetInf import *


# Notes:
# need class models - models of stuff before & after verbs
# before: model(universe, interpretation of nouns -- user input ? (interpretation fn))
# truth of sentences (subset) - models satisfaction
# user input model? -- interface proof system w model -- user input tf (countermodel like in class)
# proof or countermodel

# something like algo 2.33?
class Model:

    # output is going to be a couter-model, input will be the same as what the user did for other class (engine)
    def __init__(self, set, interpn):
        self.uni = set
        self.interpn = interpn
        # notes: wanna gen everything that has compliment in them, generate all provable ones
        # if contrad, break
        # orthoposet
        # some x are y -> x and y both state

    def generate(self):
        # of the all logic
        sentences = []
        mydict = self.interpn
        for noun in self.interpn:
            for othern in self.interpn:
                if mydict[noun].issubset(mydict[othern]):
                    sentences.append(('a', noun, othern))
        return sentences

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
'''
    def echecker(self, lon):
        for key in meaning:
            for val in meaning[key]:
                if "non" in val:
                    if

    def sfinder(self, lon):

    def countermodel(self, lot, target):
        t = target[0]
        lop = [(x, y) for _,x,y in lot]
        if t == 'a':
        # case 1 all logic
        else:
        # case 2
        echecker(lon)


    def checkcon(self, lot):
        verbs = []
        raw_vars = set()
        provables = syllogistic.provables(verbs, raw_vars)
        for phi in lot:
            nphi = self.semanticn(phi)
            if nphi in lot:
                database = Database(self.uni, lot, lov, meaning)
                Engine(rules, database, phi).gen_tf(meaning)
                Engine(rules, database, nphi).gen_tf()
                print("Since the assumptions are inconsistent, anything follows")
                break
        else:
            countermodel()
'''



    # if this list derives both o and o-bar
