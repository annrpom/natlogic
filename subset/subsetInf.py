# a statement is a tuple where r is a tag and var1 and var2 are variables
# class Statement:
#     def __init__(self, tag, var1, var2):
#         self.tag = tag
#         self.var1 = var1
#         self.var2 = var2
import itertools


# class represents inference rule
class Rule:
    def __init__(self, name, premises, conclusion):
        self.name = name
        self.premises = premises
        self.conclusion = conclusion

    # possibilities : Database -> Database
    # returns only the possible tag facts in the database that can be used w rule
    # this is for reducing the amt of possibilities we can have
    # TODO right now we are just representing a database as a set of tuples, ask if need change, maybe also doesnt need
    # TODO to be in this class, bad OOP?
    def possibilities(self, database):
        valid_tags = set(statement[0] for statement in self.premises)  # set of all tags in premise
        possible = filter(
            lambda tf: not tf[0] in valid_tags, database)  # filters out all tags facts in database that don't work
        return possible  # also from this, we know if the len(possible) < len(premises), rule not applicable

    # apply : Database -> TagFacts
    # returns the possible TagFacts that can be generated from Database
    def apply(self, database):
        consider = self.possibilities(database)
        if len(consider) < len(self.premises):
            return {}
        else:
            if len(self.premises) == 0:  # axiom, only rule w empty premise list
                return 0



    # gives u conclusion based off of premises
    """
    def apply(self, facts):
        if len(self.premises) != len(facts):
            raise ValueError("Argument length mismatch")
        if not all(prem_tag == fact_tag for (prem_tag, _, _), (fact_tag, _, _) in zip(self.premises, facts)):
            raise ValueError("Tag mismatch")
        # rewrite ?, either document code VERY well or write a more lengthy code
        s = [var for var, _ in
             set((v, n)
                 for (_, v1, v2), (_, n1, n2) in zip(self.premises, facts)
                 for v, n in [(v1, n1), (v2, n2)])]
        if len(s) != len(set(s)):
            raise ValueError("Input not applicable to given Rule")
    """


# class represents database: universe and tagfacts
class Database:
    def __init__(self, universe, tagfacts):
        self.universe = universe
        self.tagfacts = tagfacts


# class represents engine itself
class Engine:
    def __init__(self, rules, database, target):
        self.rules = rules
        self.database = database
        self.target = target

# user will input list of rules, database, and target
# we want to be able to output tree or list showing all the possible
# rule applications
