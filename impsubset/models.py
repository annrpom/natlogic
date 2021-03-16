# Notes:
# need class models - models of stuff before & after verbs
# before: model(universe, interpretation of nouns -- user input ? (interpretation fn))
# truth of sentences (subset) - models satisfaction
# user input model? -- interface proof system w model -- user input tf (countermodel like in class)
# proof or countermodel

# something like algo 2.33?
class Model:

    def __init__(self, set, interpfn):
        self.uni = set
        self.fn = interpfn
        # notes: wanna gen everything that has compliment in them, generate all provable ones
        # if contrad, break
        # orthoposet
        # some x are y -> x and y both state

    def generate(self, nouns):
        # of the all logic
        sentences = [('a', n, n) for n in nouns]

