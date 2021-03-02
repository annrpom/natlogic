from subsetInf import *
import re


def equal(a, b):
    # https://stackoverflow.com/questions/16474848/python-compare-strings-ignore-special-characters
    # Ignore non-space and non-word characters
    regex = re.compile(r'[^\s\w]')
    return regex.sub('', a) == regex.sub('', b)


def allverbs(term1, term2):
    lot1 = term1.term.split("(")
    lot2 = term2.term.split("(")
    temp = set(lot1 + lot2)
    relative = []  # all of the rcs
    for word in temp:
        if len(word.split(")")) == 1:
            relative.append(word)
    return relative


def change(verb, clause, rc):
    tbl = table(rc, meaning)
    return tbl[verb][clause]


def convert(term1, term2):
    relative = allverbs(term1, term2)
    t1 = term1.subterms  # this is the final dict
    t2 = term2.subterms
    i = len(t1)
    for t in t2.values():
        t1[i] = t
        i += 1
    t1[i] = "error"
    meaningof = table(relative, t1)
    r1 = term1.subterms[0]
    r1 = r1.split('(')[0]
    r2 = term2.subterms[0]
    r2 = r2.split('(')[0]
    v1 = meaningof[r1][1]
    v2 = meaningof[r2][(len(t1) // 2) + 1]
    return v1, v2


def table(rc, dictitems):
    index = len(dictitems)
    value = 6
    loc = {}
    for clause in rc:
        templ = []
        for i in range(index):
            word = clause + dictitems[i]
            for key in dictitems:
                if equal(word, dictitems[key]):
                    value = key
            templ.append(value)
            value = 6
        loc[clause] = templ
    return loc


class R:
    def __repr__(self):
        return "R(" + self.term + ")"

    def __init__(self, term):
        los = [term]
        curr = term
        while True:
            try:
                inner = re.search('\(([^)]+)', curr).group(1)
                # can use list - will have to rewrite
                if len(inner) > 1:
                    los.append(inner + ")")
                else:
                    los.append(inner)
                curr = inner
            except AttributeError:
                break
        i = 0
        subterms = {}
        for t in los:
            subterms[i] = t
            i += 1
        self.subterms = subterms
        self.term = term


class N(R):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "N(" + self.val + ")"

    def negate(self, setsize):
        self.val = (self.val + setsize / 2) % setsize
