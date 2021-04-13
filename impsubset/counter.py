from subsetInf import *
from partialfn import *
from models import *

# for S dagger

axiom = Rule('axiom', [], ('a', 'x', 'x'))
barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
some1 = Rule('some1', [('i', 'x', 'y')], ('i', 'x', 'x'))
some2 = Rule('some2', [('i', 'x', 'y')], ('i', 'y', 'x'))
zero = Rule('zero', [('a', 'x', N('x'))], ('a', 'x', 'y'))  # states in orthoposet
one = Rule('one', [('a', N('x'), 'x')], ('a', 'y', 'x'))  # states in orthoposet
#anti = Rule('anti', [('a', 'x', 'y')], ('a', R('y'), R('x')))
#x = Rule('x', [('a', 'x', 'y'), ('i', R('x'), 'y')], "any")
#down = Rule('down', [('a', 'x', R('y')), ('a', 'z', 'y')], ('a', 'x', R('z')))

rules = [axiom, barbara, darii, some1, some2, one, zero]
# need syntax w verbs, cannot define own but there was list -- possibility,
# gen of rules for user made up
print("Hello. Welcome to the model constructor")
meaning = {}  # dict
print("Please enter your list of premises. Press tab when finished.")
print("These should be in the form all _ are _ OR some _ are _")
lop = []
verbs = []  # verbs that exist
while True:
    prem = input("Enter a premise and then hit ENTER or just press ENTER if finished\n")
    if prem == '':
        break
    lop.append(prem)
lop = set(lop)
raw_vars = set()
print("Generated below are all of the provable tagfacts when given your premises:")
non_flag = False
i = 0
for prem in lop:
    t, w1, _, w2 = prem.split()
    if len(w1) > 1:
        if "non-" in w1:
            w1 = w1[4]
            non_flag = True
        else:
            add(w1, meaning)
            verbs += getverb(w1)
    if len(w2) > 1:
        if "non-" in w2:
            w2 = w2[4]
            non_flag = True
        else:
            add(w2, meaning)
            verbs += getverb(w2)
    raw_vars.add(w1)
    raw_vars.add(w2)
raw_vars = sorted(raw_vars)
for var in raw_vars:
    meaning[i] = var
    i += 1
j = len(meaning)
for val in meaning.values():
    if val in raw_vars:
        raw_vars.remove(val)
for var in raw_vars:
    meaning[j] = var
    j += 1

if non_flag:
    nons = ["non-" + var for var in meaning.values()]
    for item in nons:
        meaning[i] = item
        i += 1
relatives = []
for v in verbs:
    sub = [v + "(" + var + ")" for var in meaning.values()]
    relatives += sub
for item in relatives:
    if item in meaning.values():
        pass
    else:
        meaning[i] = item
        i += 1
tf = []
universe = [x for x in range(len(meaning))]
for prem in lop:
    tag, w1, _, w2 = prem.split()
    ind1 = [ind for ind, word in meaning.items() if word == w1]
    ind2 = [ind for ind, word in meaning.items() if word == w2]
    if tag == "all":
        tag = 'a'
    elif tag == "some":
        tag = 'i'
    tf.append((tag, ind1[0], ind2[0]))
database = Database(universe, set(tf), verbs, meaning)
engine = Engine(rules, database, None)
provables = engine.provable_tf()
model = Model(provables, engine)
for tf in provables:
    t, v1, v2 = tf
    nv1 = meaning[v1]
    nv2 = meaning[v2]
    if t == 'a':
        t = "all "
    elif t == "i":
        t = "some "
    print(t + nv1 + " are " + nv2)
# have to fix by maintaining condition that target is in dict, double check w rules
# code pertaining to translating the target
target = input("Enter a target\n")
ttag, tw1, _, tw2 = target.split()
try:
    ind1 = [ind for ind, word in meaning.items() if word == tw1]
    ind2 = [ind for ind, word in meaning.items() if word == tw2]
    if ttag == "all":
        target = ('a', ind1[0], ind2[0])
    elif ttag == "some":
        target = ('i', ind1[0], ind2[0])
except:
    print("No proof can be generated")

engine = Engine(rules, database, target)
model = Model(provables, engine)
model.gencm()

"""
Test on
all a z
all z a
all a non-b
all c b
all non-c d
some non-b non-a
some non-c b

target is all d non-c
"""