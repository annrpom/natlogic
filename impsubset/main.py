from subsetInf import *
from partialfn import *

barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
axiom = Rule('axiom', [], ('a', 'x', 'x'))
junk = Rule('junk', [('e', 'x', 'y'), ('e', 'y', 'x'), ('o', 'y', 'x')], ('u', 'x', 'y'))
rules = [barbara, darii, axiom, junk]

universe = [x for x in range(5)]
t1 = ('a', 0, 2)
t2 = ('a', 2, 3)
t3 = ('a', 2, 4)
t4 = ('a', 4, 1)
t5 = ('e', 3, 3)
t6 = ('i', 3, 2)
t7 = ('i', 0, 3)
tagfacts = [t1, t2, t3, t4, t5, t6, t7]
database = Database(universe, set(tagfacts))
target = ('i', 3, 3)
engine = Engine(rules, database, target)

print()
print("for another example")
# this is to make axiom works the way we want it to
target = ('a', 4, 4)
engine = Engine(rules, database, target)

print()
print("another one")
# should not be found
target = ('y', 1, 2)
engine = Engine(rules, database, target)

print()
print("another simple example")
# double check this
t1 = ('e', 2, 4)
t2 = ('e', 4, 2)
t3 = ('o', 4, 2)
tagfacts = [t1, t2, t3]
database = Database(universe, set(tagfacts))
target = ('u', 2, 4)
engine = Engine(rules, database, target)

print()
print("a more complex example")
t1 = ('a', 6, 7)
t2 = ('a', 7, 1)
t3 = ('a', 3, 6)
t4 = ('i', 3, 2)
tagfacts = [t1, t2, t3, t4]
database = Database(universe, set(tagfacts))
target = ('i', 1, 2)
engine = Engine(rules, database, target)

print()
t1 = ('a', 0, 1)
t2 = ('a', 1, 2)
t3 = ('a', 2, 3)
t4 = ('a', 3, 4)
tagfacts = [t1, t2, t3, t4]
database = Database(universe, set(tagfacts))
target = ('a', 0, 4)
engine = Engine(rules, database, target)

print("hello")
test = R("see-a(like-a(x))")
print(test.subterms)

print("hello")
test1 = R("see-a(like-a(x))")
test2 = R("see-a(like-a(y))")
rc = allverbs(R('x'), R('y'))
print(convert(test1, test2))
verb(1, table(allverbs()))



