from subsetInf import *

axiom = Rule('axiom', [], ('a', 'x', 'x'))
barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
some1 = Rule('some1', [('i', 'x', 'y')], ('i', 'x', 'x'))
some2 = Rule('some2', [('i', 'x', 'y')], ('i', 'y', 'x'))
zero = Rule('zero', [('a', 'x', n('x'))], ('a', 'x', 'y'))
one = Rule('one', [('a', n('x'), 'x')], ('a', 'y', 'x'))
anti = Rule('anti', [('a', 'x', 'y')], ('a', n('y'), n('x')))
x = Rule('x', [('a', 'x', 'y'), ('i', n('x'), 'y')], any)
rules = [axiom, barbara, darii, some1, some2, zero, one, anti, x]

print("Please enter your list of premises. Press tab when finished.")
print("These should be in the form all _ _, some _ _, or no _ _")
lop = []
while True:
    prem = input("Enter a premise and then hit ENTER or press ENTER if finished")
    if prem == '':
        break
    lop.append(prem)
lop = set(lop)
target = input("Enter a target")
extraction = {}
i = 0
for prem in lop:
    _, w1, w2 = prem.split()
    extraction[i] = w1
    i += 1
    extraction[i] = w2
    i += 1

for num in range(i):
    var = extraction[num]
    extraction[num + i] = "non-" + var

tf = []
universe = [x for x in range(len(extraction) + 1)]
lop.add(target)
for prem in lop:
    tag, w1, w2 = prem.split()
    ind1 = [ind for ind, word in extraction.items() if word == w1]
    ind2 = [ind for ind, word in extraction.items() if word == w2]
    if prem == target:
        if tag == "all":
            ttarget = ('a', ind1, ind2)
        elif tag == "some":
            ttarget = ('i', ind1, ind2)
    else:
        if tag == "all":
            tf.append(('a', ind1, ind2))
        elif tag == "some":
            tf.append(('i', ind1, ind2))
lop.remove(target)

database = Database(universe, tf)
engine = Engine(rules, database, ttarget)
engine.gen_tf()


