import itertools
from text_image import *

# this is the dictionary that keeps track of the proofs
ans = {}


# class represents inference rule
class Rule:
    # a Rule is a Rule(String, [ListOf TagFacts], TagFact)
    def __init__(self, name, premises, conclusion):
        self.name = name
        self.premises = premises
        self.conclusion = conclusion

    def __str__(self):
        return self.name + " with premises " + str(self.premises) + " and conclusion " + str(self.conclusion)

    # valid_tags: self -> [SetOf Chars]
    # returns the set of all tags that occur in the premise
    def valid_tags(self):
        return set(statement[0] for statement in self.premises)

    # valid_vars: self -> [SetOf Chars]
    # returns the set of all variables that occur in the premise
    def valid_vars(self):
        vvars = set()
        for tf in self.premises:
            _, v1, v2 = tf
            vvars.add(v1)
            vvars.add(v2)
        return vvars

    # possibilities : Database -> [SetOf TagFacts]
    # returns only the possible tag facts in the database that can be used w rule
    # this is for reducing the amt of possibilities we can have
    def possibilities(self, database):
        possible = set(
            tf for tf in database.lot if
            tf[0] in self.valid_tags())  # filters out nonvalid tf based on tag
        return possible  # also from this, we know if the len(possible) < len(premises), rule not applicable

    # combs : [SetOf TagFacts] -> Iterator
    # returns all possible permutations of all tags
    def combs(self, poss_tf):
        lim = len(self.premises)  # this is the lim for the inner list of tf
        return itertools.product(poss_tf, repeat=lim)

    # apply : Database -> [ListOf TagFacts]
    # returns the possible TagFacts that can be generated from Database
    def apply(self, database):
        if len(self.premises) == 0:  # axiom, only rule w empty premise list
            tfl = [('a', n, n) for n in database.universe]
            for item in tfl:
                ans[item] = ("axiom", [])
            return tfl
        else:
            tfl = []
            for poss in self.combs(self.possibilities(database)):
                my_dict = {}
                for tf, ptf in zip(poss, self.premises):
                    t, v1, v2 = tf
                    pt, pv1, pv2 = ptf
                    if isinstance(pv1, N):  # for our rule one
                        nx = N(v2)
                        nx.negate(len(database.universe))
                        if nx.val == v1:
                            for i in database.universe:
                                child_pt = (t, i, v2)
                                ans[child_pt] = (self.name, [])
                                tfl.append(child_pt)
                    elif isinstance(pv2, N):
                        nx = N(v1)
                        nx.negate(len(database.universe))
                        if nx.val == v2:
                            for i in database.universe:
                                child_pt = (t, v1, i)
                                ans[child_pt] = (self.name, [])
                                tfl.append(child_pt)
                    elif self.name == 'anti':
                        nx = N(v1)
                        ny = N(v2)
                        nx.negate(len(database.universe))
                        ny.negate(len(database.universe))
                        child_pt = (t, ny.val, nx.val)
                        ans[child_pt] = (self.name, [])
                        tfl.append(child_pt)
                    else:
                        if t != pt:
                            break
                        if pv1 in my_dict:
                            if my_dict[pv1] != v1:
                                break
                        if pv2 in my_dict:
                            if my_dict[pv2] != v2:
                                break
                        my_dict[pv1] = v1
                        my_dict[pv2] = v2
                else:
                    if len(my_dict) == len(self.valid_vars()):
                        t, v1, v2 = self.conclusion
                        child_pt = (t, my_dict[v1], my_dict[v2])
                        if child_pt not in ans.keys():
                            ans[child_pt] = (self.name, poss)
                        tfl.append(child_pt)
            return tfl


class N:
    def __init__(self, val):
        self.val = val

    def negate(self, setsize):
        self.val = (self.val + setsize / 2) % setsize


# class represents database: universe and set of tagfacts
class Database:
    def __init__(self, universe, lot):
        self.universe = universe
        self.lot = lot
        for tf in lot:
            if tf not in ans.keys():
                ans[tf] = None

    def size(self):
        return len(self.lot)


# class represents engine itself
class Engine:
    def __init__(self, rules, database, target):
        self.rules = rules
        self.database = database
        self.target = target
        self.size = database.size()

    # generates and prints the proof
    def gen_proof(self, target):
        if target in ans.keys():
            if ans[target] is None:
                return []
            else:
                lop = [(target, ans[target])]
                newtarget = ans[target][1]
                for tf in newtarget:
                    lop += self.gen_proof(tf)
                return lop
        else:
            return []

    def print_proof(self, myDict):
        lop = self.gen_proof(self.target)
        lop.reverse()
        i = 1
        nums_used = []
        for item in lop:
            print(i, end=' ')
            res, parent = item
            rule, tf = parent
            tf = list(tf)
            for item in tf:
                nums_used.append(i)
                t, v1, v2 = item
                translated = (t, myDict[v1], myDict[v2])
                print(translated, "given")
                i += 1
                print(i, end=' ')
            t, v1, v2 = res
            tv1 = myDict[v1]
            tv2 = myDict[v2]
            english = ""
            if t == 'a':
                english += "all "
            if t == 's':
                english += "some "
            english = english + tv1 + " are " + tv2
            print(english + " uses " + rule + " from applications of " + str(nums_used))
            nums_used = []
            i += 1

    # (U None TagFacts) (Dict Num String) -> String
    def pretty_print(self, myDict):
        def nodeStr(node):
            tag    = "All " if node[0] == 'a' else "I "
            first  = myDict[node[1]] if isinstance(node[1],int) else node[1]
            second = myDict[node[2]] if isinstance(node[2],int) else node[2]
            return tag + first + " " + second
        def pretty_print_internal(node):
            rec      = ans[node]
            rule     = "given" if not rec else rec[0]
            parents  = [] if not rec else rec[1]
            subtrees = TextImage("")
            nodeStrg = nodeStr(node)
            for parent in parents:
                subtrees = subtrees.beside(pretty_print_internal(parent), 2)
            if(subtrees.width > len(nodeStrg)):
                bar_rule = "-" * (subtrees.width + 2)
                return subtrees.aboveStr(bar_rule).beside(TextImage([rule]),1).aboveStr(nodeStrg)
            else:
                bar_rule = "-" * (len(nodeStrg) + 2)
                return subtrees.above(TextImage(bar_rule).aboveStr(nodeStrg).beside(TextImage([rule,""]), 1))
        return str(pretty_print_internal(self.target))

    # generate tag_facts until cannot, stops when prev size is == to curr size of database
    def gen_tf(self, myDict):
        while True:
            self.size = self.database.size()
            for rule in self.rules:
                generated = rule.apply(self.database)  # this produces a [ListOf ProofTrees]
                self.database.lot.update(generated)
                if self.target in ans.keys():
                    print("Proof was found!")
                    self.print_proof(myDict)
                    return
            if self.size == self.database.size():
                print("Nothing was found")
                break
        ans.clear()

    def provable_tf(self):
        provables = []
        while True:
            self.size = self.database.size()
            for rule in self.rules:
                gen = rule.apply(self.database)
                self.database.lot.update(gen)
            if self.size == self.database.size():
                for item in ans.keys():
                    if ans[item] is None:
                        pass
                    else:
                        for val in ans[item][1]:
                            provables.append(val)
                        provables.append(item)
                return provables

