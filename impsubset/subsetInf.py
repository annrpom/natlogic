import itertools
from partialfn import *
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

    # determines if rule is a partial function
    def pf_huh(self):
        result = False
        for phi in self.premises:
            for item in phi:
                if isinstance(item, R):
                    result = True
        for item in self.conclusion:
            if isinstance(item, R):
                result = True
        return result

    # apply : Database -> [ListOf TagFacts]
    # returns the possible TagFacts that can be generated from Database
    # abstract usage of N and R for the partialfn part
    def apply(self, database):
        if self.name == "axiom":  # axiom should not be applied to whole database - needs to factor in for some
            return axiom(database)
        else:
            tfl = []
            for poss in self.combs(self.possibilities(database)):
                my_dict = {}
                for tf, ptf in zip(poss, self.premises):
                    t, v1, v2 = tf
                    pt, pv1, pv2 = ptf
                    if self.pf_huh():
                        val = partfn(database, tf, ptf, tfl)
                        if val == 0:
                            if isinstance(pv2, R):
                                my_dict[pv1] = v1
                                my_dict[pv2.term] = v2
                            else:
                                my_dict[pv1] = v1
                                if pv2 in my_dict:
                                    tbl = table(database.lov, database.meaning)
                                    v = verb(v2, tbl)
                                    if change(v, v2, tbl) == my_dict[pv2]:
                                        my_dict['z'] = change(v, v1, tbl)
                                        child_pt = (t, my_dict['x'], my_dict['z'])
                                        if child_pt not in ans.keys():
                                            ans[child_pt] = (self.name, poss)
                                        tfl.append(child_pt)
                                        break
                                    else:
                                        break
                                else:
                                    break
                        else:
                            break
                    elif self.name == 'anti':
                        anti(database, tf, ptf, tfl)
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
                        if isinstance(v2, R):
                            v2 = v2.term
                        child_pt = (t, my_dict[v1], my_dict[v2])
                        if child_pt not in ans.keys():
                            ans[child_pt] = (self.name, poss)
                        tfl.append(child_pt)
            return tfl


# class represents database: universe and set of tagfacts
class Database:
    def __init__(self, universe, lot, lov, meaning):
        self.universe = universe
        self.lot = lot
        self.lov = lov
        self.meaning = meaning
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
                if t == 'a':
                    t = "all "
                if t == 'i':
                    t = "some "
                translated = t + myDict[v1] + " are " + myDict[v2]
                print(translated, "-- given")
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

    # generate tag_facts until cannot, stops when prev size is == to curr size of database
    def gen_tf(self):
        while True:
            self.size = self.database.size()
            for rule in self.rules:
                generated = rule.apply(self.database)  # this produces a [ListOf ProofTrees]
                self.database.lot.update(generated)
                if self.target in ans.keys():
                    print("Proof was found!")
                    self.print_proof(self.database.meaning)
                    ans.clear()
                    return
            if self.size == self.database.size():
                print("Nothing was found")
                return False
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


# Notes:
# need class models - models of stuff before & after verbs
# before: model(universe, interpretation of nouns -- user input ? (interpretation fn))
# truth of sentences (subset) - models satisfaction
# user input model? -- interface proof system w model -- user input tf (countermodel like in class)
# proof or countermodel
def axiom(database):
    tfl = [('a', n, n) for n in database.universe]
    for item in tfl:
        ans[item] = ("axiom", [])
    return tfl


def partfn(database, tf, ptf, tfl):
    t, v1, v2 = tf
    pt, pv1, pv2 = ptf
    if isinstance(pv1, N):  # for our rule one
        nx = N(v2)
        nx.negate(len(database.universe))
        if nx.val == v1:
            for i in database.universe:
                if i == v2:
                    continue
                child_pt = (t, i, v2)
                ans[child_pt] = ("one", [])
                tfl.append(child_pt)
    elif isinstance(pv2, N):
        nx = N(v1)
        nx.negate(len(database.universe))
        if nx.val == v2:
            for i in database.universe:
                if i == v1:
                    continue
                child_pt = (t, v1, i)
                ans[child_pt] = ("zero", [])
                tfl.append(child_pt)
    else:
        return 0


def anti(database, tf, ptf, tfl):
    t, v1, v2 = tf
    pt, pv1, pv2 = ptf
    nx = N(v1)
    ny = N(v2)
    nx.negate(len(database.universe))
    ny.negate(len(database.universe))
    child_pt = (t, ny.val, nx.val)
    ans[child_pt] = ("anti", [])
    tfl.append(child_pt)
    if len(database.lov):
        for v in database.lov:
            child_pt = (t, change(v, v1, verbs), change(v, v2, verbs))
            ans[child_pt] = ("anti", [])
            tfl.append(child_pt)
