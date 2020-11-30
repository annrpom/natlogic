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
        print(type(prooftrees))
        edge_pt = [t8, t9, t10, t11, t12]
        database = Database(universe, prooftrees)
        edge_dat = Database(universe, edge_pt)

        barbara_tf = prooftrees[:4]
        darri_tf = set(prooftrees[:4] + prooftrees[5:])
        axiom_tf = set()
        junk_tf = {('e', 3, 3)}
        swap_tf = set(edge_pt[:2])
        most_tf = set(edge_pt[:3])
        no2_tf = {('o', 2, 2)}

        self.assertEqual(barbara_tf, barbara.possibilities(database))
        #self.assertEqual(darri_tf, darii.possibilities(database))
        #self.assertEqual(axiom_tf, axiom.possibilities(database))
        #self.assertEqual(junk_tf, junk.possibilities(database))
        #self.assertEqual(swap_tf, swap.possibilities(edge_dat))
        #self.assertEqual(most_tf, most.possibilities(edge_dat))
        #self.assertEqual(no2_tf, no2.possibilities(edge_dat))

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
        tagfacts = [('a', 0, 2), ('a', 2, 3), ('a', 2, 4), ('a', 4, 1), ('e', 3, 3), ('i', 0, 3), ('i', 3, 2)]
        edge_tf = [('a', 0, 3), ('a', 1, 4), ('m', 2, 1), ('s', 0, 3), ('o', 2, 2)]
        database = Database(universe, tagfacts)
        edge_dat = Database(universe, edge_tf)

        barbara_app = [('a', 0, 3), ('a', 0, 4), ('a', 2, 1)]
        darii_app = [('i', 2, 3)]
        axiom_app = [('a', 0, 0), ('a', 1, 1), ('a', 2, 2), ('a', 3, 3), ('a', 4, 4)]

        self.assertEqual(set(barbara_app), set(barbara.apply(database)))
        self.assertEqual(darii_app, darii.apply(database))
        self.assertEqual(axiom_app, axiom.apply(database))


if __name__ == '__main__':
    unittest.main()