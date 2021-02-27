from subsetInf import *

# if i could make a change - change rule to abstract class and have NRule and regRule stem from it

axiom = Rule('axiom', [], ('a', 'x', 'x'))
barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
some1 = Rule('some1', [('i', 'x', 'y')], ('i', 'x', 'x'))
some2 = Rule('some2', [('i', 'x', 'y')], ('i', 'y', 'x'))
zero = Rule('zero', [('a', 'x', N('x'))], ('a', 'x', 'y'))
one = Rule('one', [('a', N('x'), 'x')], ('a', 'y', 'x'))
anti = Rule('anti', [('a', 'x', 'y')], ('a', N('y'), N('x')))
x = Rule('x', [('a', 'x', 'y'), ('i', N('x'), 'y')], any)
lor = [axiom, barbara, darii, some1, some2, one, zero, anti, x]

print("Hello. Welcome to the syllogistic inference evaluator.")
print("Examples are coming soon THEY WILL BE GENERATED HERE")
print("-".join("-" * 10))
print("Below are a list of rules to choose from, please type in which rules you would like this engine to have.")
print("(Put these on one line, separated by commas. Press enter when finished.)\n")
print(str(axiom) + "\n" + str(barbara) + "\n" + str(darii) + "\n" + str(some1))
print(str(some2) + "\n" + str(zero) + "\n" + str(one) + "\n" + str(anti) + "\n" + str(x) + "\n")
ulor = input("Enter choices below:\n")
ulor = ulor.split(", ")
rules = []
for rule in ulor:
    for setrule in lor:
        if rule == setrule.name:
            rules.append(setrule)
print("Please enter your list of premises. Press tab when finished.")
print("These should be in the form all _ are _ OR some _ are _")
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
    t, w1, _, w2 = prem.split()
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
universe = [x for x in range(len(extraction))]
for prem in lop:
    tag, w1, _, w2 = prem.split()
    ind1 = [ind for ind, word in extraction.items() if word == w1]
    ind2 = [ind for ind, word in extraction.items() if word == w2]
    if tag == "all":
        tf.append(('a', ind1[0], ind2[0]))
    elif tag == "some":
        tf.append(('i', ind1[0], ind2[0]))

database = Database(universe, set(tf))
engine = Engine(rules, database, None)
provables = engine.provable_tf()
for tf in provables:
    t, v1, v2 = tf
    nv1 = extraction[v1]
    nv2 = extraction[v2]
    print((t, nv1, nv2))
print()

# have to fix by maintaining condition that target is in dict, double check w rules
# code pertaining to translating the target
target = input("Enter a target\n")
ttag, tw1, _, tw2 = target.split()
try:
    ind1 = [ind for ind, word in extraction.items() if word == tw1]
    ind2 = [ind for ind, word in extraction.items() if word == tw2]
    if ttag == "all":
        target = ('a', ind1[0], ind2[0])
    elif ttag == "some":
        target = ('i', ind1[0], ind2[0])
except:
    print("No proof can be generated")

engine = Engine(rules, database, target)
engine.gen_tf(extraction)
print("\n\n")
print(engine.pretty_print(extraction))
