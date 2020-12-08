from subsetInf import *

barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
axiom = Rule('axiom', [], ('a', 'x', 'x'))
junk = Rule('junk', [('e', 'x', 'y'), ('e', 'y', 'x'), ('o', 'y', 'x')], ('u', 'x', 'y'))
rules = [barbara, darii, axiom, junk]

universe = [x for x in range(5)]
t1 = ProofTree('a', 0, 2)
t2 = ProofTree('a', 2, 3)
t3 = ProofTree('a', 2, 4)
t4 = ProofTree('a', 4, 1)
t5 = ProofTree('e', 3, 3)
t6 = ProofTree('i', 3, 2)
t7 = ProofTree('i', 0, 3)


prooftrees = [t1, t2, t3, t4, t5, t6,t7]
database = Database(universe, prooftrees)

target = ProofTree('i', 3, 3)

engine = Engine(rules, database, target)

ans = engine.gen_tf()
print(ans)
print("THIS IS THE PRINT")
print(ans.follow_previous())
