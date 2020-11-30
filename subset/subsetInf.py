import itertools


# might need this to have a pointer back to the creation
class ProofTree:
    def __init__(self, tag, var1, var2):
        self.node = (tag, var1, var2)
        self.parents = None  # this will need to be calculated after something has been applied

    def set_parents(self, pt):
        self.parents = pt

    def get_tf(self):
        return self.node

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, ProofTree):
            return self.node == other.node
        return NotImplemented

    def __str__(self):
        return self.node.__str__()

    def __hash__(self):
        return id(self.node)

    # follow_previous: self -> List
    # returns a list of the statements used to get to curr statement, if any
    # this will be for printing and keeping track of things
    def follow_previous(self):
        encountered = []
        if self.parents is None:
            return encountered.append(self)
        else:
            encountered = self.parents.follow_previous()
            encountered.append(self)
            return encountered


# class represents inference rule
class Rule:
    def __init__(self, name, premises, conclusion):
        self.name = name
        self.premises = premises
        self.conclusion = conclusion

    # valid_tags: self = [SetOf Chars]
    def valid_tags(self):
        return set(statement[0] for statement in self.premises)  # set of all tags in premise

    # valid_vars: self = [SetOf Chars]
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
    # TODO to be in this class, bad OOP?
    def possibilities(self, database):
        possible = set(
            tf for tf in database.get_tagfacts() if tf[0] in self.valid_tags())  # filters out nonvalid tf based on tag
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
            return [('a', n, n) for n in database.universe]
        else:
            my_dict = {}
            tfl = []
            for poss in self.combs(self.possibilities(database)):
                for tf, ptf in zip(poss, self.premises):
                    t, v1, v2 = tf
                    pt, pv1, pv2 = ptf
                    if t != pt:
                        break
                    if pv1 in my_dict:
                        if my_dict.get(pv1) != v1:
                            break
                    if pv2 in my_dict:
                        if my_dict.get(pv2) != v2:
                            break
                    my_dict[pv1] = v1
                    my_dict[pv2] = v2
                if len(my_dict) == len(self.valid_vars()):
                    t, v1, v2 = self.conclusion
                    tfl.append((t, my_dict[v1], my_dict[v2]))
                my_dict = {}
            return tfl


# class represents database: universe and prooftrees
class Database:
    def __init__(self, universe, prooftrees):
        self.universe = universe
        self.prooftrees = prooftrees

    def get_tagfacts(self):
        tf = []
        for pt in self.prooftrees:
            tf += [pt.get_tf()]
        return tf

    def size(self):
        return len(self.get_tagfacts())

    # get_tag : TagFact -> TagFact
    # returns the actual tagfact obj when shallow tf is given
    def get_tag(self, tf):
        for tagfact in self.get_tagfacts():
            tt, tv1, tv2 = tf
            ot, ov1, ov2 = tagfact
            if tt == ot and tv1 == ov1 and tv1 == ov1:
                return tagfact

    # contain : TagFact -> Boolean
    def contain(self, tf):
        ct = False
        for tagfact in self.get_tagfacts():
            tt, tv1, tv2 = tf
            ot, ov1, ov2 = tagfact
            ct = tt == ot and tv1 == ov1 and tv1 == ov1
        return ct


# class represents engine itself
class Engine:
    def __init__(self, rules, database, target):
        self.rules = rules
        self.database = database
        self.target = target
        self.size = database.size()

    # generate tag_facts until cannot, stops when prev size is == to curr size of database
    def gen_tf(self):
        flag = 0
        while True:
            self.size = self.database.size()
            for rule in self.rules:
                generated = rule.apply(self.database)
                self.database.tagfacts += generated
                if self.database.contain(self.target):
                    flag = 1
                    break
            if self.size == self.database.size():
                break
        if flag:
            return self.database.get_tag(self.target)  # wishlist method
        else:
            print("Not Avail")

# need to find the final result from this calculation

# user will input list of rules, database, and target
# we want to be able to output tree or list showing all the possible
# rule applications
