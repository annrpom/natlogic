# a statement is a tuple where r is a tag and var1 and var2 are variables
# class Statement:
#     def __init__(self, tag, var1, var2):
#         self.tag = tag
#         self.var1 = var1
#         self.var2 = var2
import itertools


class Rule:
    def __init__(self, name, premises, conclusion):
        self.name = name
        self.premises = premises
        self.conclusion = conclusion

    # gives u conclusion based off of premises
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

# user will input list of rules, database, and target
# we want to be able to output tree or list showing all the possible
# rule applications