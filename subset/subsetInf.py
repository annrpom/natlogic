import itertools


# might need this to have a pointer back to the creation
class ProofTree:
    def __init__(self, tag, var1, var2):
        self.node = (tag, var1, var2)
        self.parents = None  # this will need to be calculated after something has been applied
        self.rule = None  # this is the rule that it took to get from its parents to self.node

    def set_parents(self, pt):
        self.parents = pt

    # self -> Tuple
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

    def set_rule(self, rule):
        self.rule = rule

    def get_parents(self):
        return self.parents

    def parent_strings(self):
        str = ""
        if self.parents is None:
            return ""
        for poss in self.parents:
            tup = poss.get_tf()
            str += tup.__str__()
        return str

    # follow_previous: self
    # returns a list of the statements used to get to curr statement, if any
    # this will be for printing and keeping track of things
    def follow_previous_helper(self):
        encountered = []
        if self is None or self.parents is None:
            print("", end='')
        else:
            for pt in self.parents:
                encountered.append(pt.follow_previous_helper())
            encountered.append(self.parent_strings() + " " + self.rule + " w/ concl: " + str(self.get_tf()))
        return encountered

    def follow_previous(self):
        encountered = self.follow_previous_helper()
        i = 0
        for pt in encountered:
            if pt is None or not pt:
                print("", end='')
            else:
                i += 1
                print(str(i), end=' ')
                if isinstance(pt, str):
                    print(pt)
                else:
                    for item in pt:
                        if not item:
                            print("", end='')
                        else:
                            print(item)

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

    # whenever i ref. TagFacts in signature, I am talking about a ProofTree
    # possibilities : Database -> [SetOf TagFacts]
    # returns only the possible tag facts in the database that can be used w rule
    # this is for reducing the amt of possibilities we can have
    # TODO to be in this class, bad OOP?
    def possibilities(self, database):
        possible = set(
            tf for tf in database.prooftrees if
            tf.get_tf()[0] in self.valid_tags())  # filters out nonvalid tf based on tag
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
            ret = []
            for n in database.universe:
                pt = ProofTree('a', n, n)
                pt.set_rule(self.name)
                ret.append(pt)
            return ret
        else:
            my_dict = {}
            tfl = []
            for poss in self.combs(self.possibilities(database)):
                for tf, ptf in zip(poss, self.premises):
                    t, v1, v2 = tf.get_tf()
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
                    child_pt = ProofTree(t, my_dict[v1], my_dict[v2])
                    child_pt.set_parents(poss)
                    child_pt.set_rule(self.name)
                    tfl.append(child_pt)
                my_dict = {}  # we use a dictionary per possibility
            return tfl


# class represents database: universe and prooftrees
class Database:
    def __init__(self, universe, prooftrees):
        self.universe = universe
        self.prooftrees = prooftrees

    def size(self):
        return len(self.prooftrees)

    # get_tag : TagFact -> TagFact
    # returns the actual tagfact obj when shallow tf is given
    def get_tag(self, tf):
        for pt in self.prooftrees:
            if tf.get_tf() == pt.get_tf():
                return pt

    # contain : self ProofTree -> Boolean
    """
    def contain(self, tf):
        ct = True
        for pt in self.prooftrees:
            tt, tv1, tv2 = tf.get_tf()
            ot, ov1, ov2 = pt.get_tf()
            ct = tt != ot or tv1 != ov1 or tv2 != ov2
        return ct
    """

    def contain(self, tf):
        return tf in self.prooftrees


# class represents engine itself
class Engine:
    def __init__(self, rules, database, target):
        self.rules = rules
        self.database = database
        self.target = target
        self.size = database.size()

    # generate tag_facts until cannot, stops when prev size is == to curr size of database
    def gen_tf(self):
        while True:
            # print("engine size", self.size, "datasize", self.database.size())
            self.size = self.database.size()
            # print("after revision", "engine size", self.size, "datasize", self.database.size(), "these will be equal")
            for rule in self.rules:
                generated = rule.apply(self.database)  # this produces a [ListOf ProofTrees]
                no_dupes = []
                for pt in generated:
                    if not self.database.contain(pt):
                        no_dupes.append(pt)
                self.database.prooftrees += no_dupes
                if self.database.contain(self.target):
                    # print("DOES THIS EVER WORK")
                    return self.database.get_tag(self.target)
            if self.size == self.database.size():
                print("nothing was found")
                break

# need to find the final result from this calculation

# user will input list of rules, database, and target
# we want to be able to output tree or list showing all the possible
# rule applications
