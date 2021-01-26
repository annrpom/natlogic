from subsetInf import *


class N:
    def __init__(self, variable):
        sign = "neg"
        if type(variable) is tuple:
            if variable[1] == "neg":
                sign = "pos"
        self.variable = (variable, sign)


axiom = Rule('axiom', [], ('a', 'x', 'x'))
barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
some1 = Rule('some1', [('i', 'x', 'y')], ('i', 'x', 'x'))
some2 = Rule('some2', [('i', 'x', 'y')], ('i', 'y', 'x'))
zero = Rule('zero', [('a', 'x', N('x'))], ('a', 'x', 'y'))
one = Rule('one', [('a', N('x'), 'x')], ('a', 'y', 'x'))
anti = Rule('anti', [('a', 'x', 'y')], ('a', N('y'), N('x')))
x = Rule('x', [('a', 'x', 'y'), ('i', N('x'), 'y')], any)
rules = [axiom, barbara, darii, some1, some2]

print("Please enter your list of premises. Press tab when finished.")
print("These should be in the form all _ _, some _ _, or no _ _")
lop = []
while True:
    prem = input("Enter a premise and then hit ENTER or just press ENTER if finished\n")
    if prem == '':
        break
    lop.append(prem)
lop = set(lop)
raw_vars = set()
print("Generated below are all of the provable tagfacts when given your premises:")
extraction = {}
i = 0
for prem in lop:
    _, w1, w2 = prem.split()
    if "non-" in w1:
        w1 = w1[4]
    if "non-" in w2:
        w2 = w2[4]
    raw_vars.add(w1)
    raw_vars.add(w2)
raw_vars = sorted(raw_vars)
for var in raw_vars:
    extraction[i] = var
    i += 1
nons = ["non-" + var for var in extraction.values()]
for item in nons:
    extraction[i] = item
    i += 1
tf = []
universe = [x for x in range(len(extraction) + 1)]
for prem in lop:
    tag, w1, w2 = prem.split()
    ind1 = [ind for ind, word in extraction.items() if word == w1]
    ind2 = [ind for ind, word in extraction.items() if word == w2]
    if tag == "all":
        tf.append(('a', ind1[0], ind2[0]))
    elif tag == "some":
        tf.append(('i', ind1[0], ind2[0]))

database = Database(universe, set(tf))
engine = Engine(rules, database, None)
engine.provable_tf()

# code pertaining to translating the target
target = input("Enter a target\n")
ttag, tw1, tw2 = target.split()
ind1 = [ind for ind, word in extraction.items() if word == tw1]
ind2 = [ind for ind, word in extraction.items() if word == tw2]
if ttag == "all":
    target = ('a', ind1[0], ind2[0])
elif ttag == "some":
    target = ('i', ind1[0], ind2[0])

engine = Engine(rules, database, target)
engine.gen_tf()
