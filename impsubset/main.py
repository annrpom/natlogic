
from models import *

barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
axiom = Rule('axiom', [], ('a', 'x', 'x'))
junk = Rule('junk', [('e', 'x', 'y'), ('e', 'y', 'x'), ('o', 'y', 'x')], ('u', 'x', 'y'))
rules = [barbara, darii, axiom, junk]


interp = {'n': set(), 'p': set([1, 3, 4]), 'q': set([1, 3])}
example = Model({1, 2, 3, 4, 5}, interp)
gen = example.generate()
print(gen)

universe = [x for x in range(3)]
model = Model(universe, {})