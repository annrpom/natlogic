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
