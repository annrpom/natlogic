from subsetInf import *

barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
axiom = Rule('axiom', [], ('a', 'x', 'x'))
junk = Rule('junk', [('e', 'x', 'y'), ('e', 'y', 'x'), ('o', 'y', 'x')], ('u', 'x', 'y'))
rules = [barbara, darii, axiom, junk]

universe = range(5)
tagfacts = [('a', 0, 2), ('a', 2, 3), ('a', 2, 4), ('a', 4, 1), ('e', 3, 3), ('i', 0, 3), ('i', 3, 2)]
database = Database(universe, tagfacts)

target = ('i', 0, 3)

engine = Engine(rules, database, target)


