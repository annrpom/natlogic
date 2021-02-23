from subsetInf import *
import re


def equal(a, b):
    # https://stackoverflow.com/questions/16474848/python-compare-strings-ignore-special-characters
    # Ignore non-space and non-word characters
    regex = re.compile(r'[^\s\w]')
    return regex.sub('', a) == regex.sub('', b)


def convert(term1, term2):
    lot1 = term1.term.split("(")
    lot2 = term2.term.split("(")
    temp = set(lot1 + lot2)
    relative = [] # all of the rcs
    for word in temp:
        if len(word.split(")")) == 1:
            relative.append(word)
    t1 = term1.subterms # this is the final dict
    t2 = term2.subterms
    i = len(t1)
    for t in t2.values():
        t1[i] = t
        i += 1
    t1[i] = "error"
    table(relative, t1)


def table(rc, dictitems):
    index = len(dictitems)
    value = 6
    loc = []
    for clause in rc:
        templ = []
        for i in range(index):
            word = clause + dictitems[i]
            for key in dictitems:
                if equal(word, dictitems[key]):
                    value = key
            templ.append(value)
            value = 6
        loc.append([clause, templ])
    print(loc)
    return loc


class R:
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

        # throw "error" at end of dict

        # make fn
