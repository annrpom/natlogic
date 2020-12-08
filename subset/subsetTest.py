import unittest
from subsetInf import *


class TestRuleMethods(unittest.TestCase):

    def test_possibilities(self):
        barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
        darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
        axiom = Rule('axiom', [], ('a', 'x', 'x'))
        junk = Rule('junk', [('e', 'x', 'y'), ('e', 'y', 'x'), ('o', 'y', 'x')], ('u', 'x', 'y'))
        swap = Rule('swap', [('a', 'x', 'y')], ('s', 'y', 'x'))
        most = Rule('most', [('m', 'x', 'y'), ('a', 'y', 'z')], ('m', 'x', 'z'))
        no2 = Rule('no2', [('o', 'x', 'x')], ('a', 'x', 'y'))
        # preMaj = Rule('pre-Maj', [('b', 'x', 'y')], ('c', 'x', 'y'), ('d', 'x', 'x')], ('b', 'y', 'x'))

        universe = [x for x in range(5)]
        t1 = ProofTree('a', 0, 2)
        t2 = ProofTree('a', 2, 3)
        t3 = ProofTree('a', 2, 4)
        t4 = ProofTree('a', 4, 1)
        t5 = ProofTree('e', 3, 3)
        t6 = ProofTree('i', 0, 3)
        t7 = ProofTree('i', 3, 2)
        t8 = ProofTree('a', 0, 3)
        t9 = ProofTree('a', 1, 4)
        t10 = ProofTree('m', 2, 1)
        t11 = ProofTree('s', 0, 3)
        t12 = ProofTree('o', 2, 2)
        prooftrees = [t1, t2, t3, t4, t5, t6, t7]
        edge_pt = [t8, t9, t10, t11, t12]
        database = Database(universe, prooftrees)
        edge_dat = Database(universe, edge_pt)

        barbara_tf = set(prooftrees[:4])
        darri_tf = set(prooftrees[:4] + prooftrees[5:])
        axiom_tf = set()
        junk_tf = {prooftrees[4]}
        swap_tf = set(edge_pt[:2])
        most_tf = set(edge_pt[:3])
        no2_tf = {ProofTree('o', 2, 2)}

        self.assertEqual(barbara_tf, barbara.possibilities(database))
        self.assertEqual(darri_tf, darii.possibilities(database))
        self.assertEqual(axiom_tf, axiom.possibilities(database))
        for e in junk_tf:
            print(e)
        for e in junk.possibilities(database):
            print(e)
        self.assertEqual(swap_tf, swap.possibilities(edge_dat))
        self.assertEqual(most_tf, most.possibilities(edge_dat))
        for e in no2_tf:
            print(e)
        for e in no2.possibilities(edge_dat):
            print(e)

    def test_apply(self):
        barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
        darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
        axiom = Rule('axiom', [], ('a', 'x', 'x'))
        junk = Rule('junk', [('e', 'x', 'y'), ('e', 'y', 'x'), ('o', 'y', 'x')], ('u', 'x', 'y'))
        swap = Rule('swap', [('a', 'x', 'y')], ('s', 'y', 'x'))
        most = Rule('most', [('m', 'x', 'y'), ('a', 'y', 'z')], ('m', 'x', 'z'))
        no2 = Rule('no2', [('o', 'x', 'x')], ('a', 'x', 'y'))
        # preMaj = Rule('pre-Maj', [('b', 'x', 'y')], ('c', 'x', 'y'), ('d', 'x', 'x')], ('b', 'y', 'x'))

        universe = [x for x in range(5)]
        t1 = ProofTree('a', 0, 2)
        t2 = ProofTree('a', 2, 3)
        t3 = ProofTree('a', 2, 4)
        t4 = ProofTree('a', 4, 1)
        t5 = ProofTree('e', 3, 3)
        t6 = ProofTree('i', 0, 3)
        t7 = ProofTree('i', 3, 2)
        t8 = ProofTree('a', 0, 3)
        t9 = ProofTree('a', 1, 4)
        t10 = ProofTree('m', 2, 1)
        t11 = ProofTree('s', 0, 3)
        t12 = ProofTree('o', 2, 2)
        prooftrees = [t1, t2, t3, t4, t5, t6, t7]
        edge_pt = [t8, t9, t10, t11, t12]
        database = Database(universe, prooftrees)
        edge_dat = Database(universe, edge_pt)

        # for the purpose of easier tests, i consider equality of prooftrees through tuples(the node)
        barbara_app = [ProofTree('a', 0, 3), ProofTree('a', 0, 4), ProofTree('a', 2, 1)]
        darii_app = [ProofTree('i', 2, 3)]
        axiom_app = [ProofTree('a', 0, 0), ProofTree('a', 1, 1), ProofTree('a', 2, 2), ProofTree('a', 3, 3),
                     ProofTree('a', 4, 4)]

        self.assertEqual({1, 2, 3}, {1, 2, 3})  # we can compare sets w assertEquals

        # however, i am still going to assert the system of parent and child works:
        print("\n")
        for e in barbara_app:
            print(e)
        print("break")
        for e in barbara.apply(database):
            print(e, "parent nodes:", e.parent_strings())
        self.assertTrue(ProofTree('a', 1, 2) == (ProofTree('a', 1, 2)))  # why why why why why

        print("\n" + "now for darii")
        for e in darii_app:
            print(e)
        print("break")
        for e in darii.apply(database):
            print(e, "parent nodes:", e.parent_strings())

        print("\n" + "now for axiom")
        for e in axiom_app:
            print(e)
        print("break")
        for e in axiom.apply(database):
            print(e)

    def test_debug(self):
        barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
        t1 = ProofTree('a', 0, 2)
        t2 = ProofTree('a', 2, 3)
        t3 = ProofTree('a', 2, 4)
        t4 = ProofTree('a', 4, 1)
        prooftrees = [t1, t2, t3, t4]
        universe = [e for e in range(5)]
        database = Database(universe, prooftrees)

        appl = barbara.apply(database)
        print("\n")
        for pt in appl:
            print(pt, "here is the parent", pt.parent_strings())
        prooftrees += appl
        print("CONCAT LISTS")
        for pt in database.prooftrees:
            print(pt)
        # try to see if my contain works
        database = Database(universe, prooftrees)
        no_dupes = []
        for pt in appl:
            if not database.contain(pt):
                no_dupes.append(pt)
        prooftrees += no_dupes
        self.assertTrue(database.contain(ProofTree('a', 0, 4)))
        self.assertTrue(ProofTree('a', 2, 1) in database.prooftrees)
        print("THERE SHOULD NOT BE ANY DUPLICATES HERE")
        for pt in prooftrees:
            print(pt)

    def test_more(self):
        barbara = Rule('barbara', [('a', 'x', 'y'), ('a', 'y', 'z')], ('a', 'x', 'z'))
        darii = Rule('darii', [('a', 'x', 'y'), ('i', 'x', 'z')], ('i', 'y', 'z'))
        t1 = ProofTree('a', 0, 2)
        t2 = ProofTree('a', 2, 3)
        t3 = ProofTree('a', 2, 4)
        t4 = ProofTree('a', 4, 1)
        t5 = ProofTree('i', 0, 3)
        prooftrees = [t1, t2, t3, t4, t5]
        universe = [e for e in range(5)]
        database = Database(universe, prooftrees)
        appl = barbara.apply(database)
        prooftrees += appl
        database = Database(universe, prooftrees)
        tf = database.get_tag(ProofTree('a', 0, 3))
        print()
        print(tf.parent_strings())
        appl = darii.apply(database)
        prooftrees += appl
        database = Database(universe, prooftrees)
        tf = database.get_tag(ProofTree('i', 3, 3))
        print("HERE")
        print(tf.parent_strings())
        for p in tf.get_parents():
            print(p.parent_strings())






if __name__ == '__main__':
    unittest.main()
