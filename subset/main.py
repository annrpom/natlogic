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

print()
print("for another example")
# this is to make axiom works the way we want it to
target5 = ProofTree('a', 4, 4)
engine5 = Engine(rules, database, target5)
ans = engine5.gen_tf()
print(ans)

print()
print("another simple example")
t1 = ProofTree('e', 2, 4)
t2 = ProofTree('e', 4, 2)
t3 = ProofTree('o', 4, 2)
pts = [t1, t2, t3]
database = Database(universe, pts)
target = ProofTree('u', 2, 4)
engine = Engine(rules, database, target)
ans = engine.gen_tf()
print(ans)
print(ans.follow_previous())

print()
print("a more complex exmple, 2 barbs and 1 darii")
t1 = ProofTree('a', 6, 7)
t2 = ProofTree('a', 7, 1)
t3 = ProofTree('a', 3, 6)
t4 = ProofTree('i', 3, 2)
pts = [t1, t2, t3, t4]
universe = [x for x in range(8)]
database = Database(universe, pts)
target = ProofTree('i', 1, 2)
engine = Engine(rules, database, target)
ans = engine.gen_tf()
print(ans)
print(ans.follow_previous())