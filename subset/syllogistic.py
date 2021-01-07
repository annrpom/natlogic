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
lop = []
while True:
    prem = input("Enter a premise and then hit ENTER or press ENTER if finished")
    if prem == '':
        break
    lop.append(prem)
lop = set(lop)
target = input("Enter a target")

