from subsetInf import *
import re


class R:
    def __init__(self, term):
        los = [term]
        curr = term
        while True:
            try:
                inner = re.search('\(([^)]+)', curr).group(1)
                # can use list - will have to rewrite
                if len(inner) > 1:
                    los.append(inner+")")
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

        # throw "error" at end of dict

        # make fn



