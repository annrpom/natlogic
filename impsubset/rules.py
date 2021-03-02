import subsetInf
from partialfn import *


def axiom(database):
    tfl = [('a', n, n) for n in database.universe]
    for item in tfl:
        subsetInf.ans[item] = ("axiom", [])
    return tfl


def partfn(database, tf, ptf, tfl):
    t, v1, v2 = tf
    pt, pv1, pv2 = ptf
    if isinstance(pv1, N):  # for our rule one
        nx = N(v2)
        nx.negate(len(database.universe))
        if nx.val == v1:
            for i in database.universe:
                child_pt = (t, i, v2)
                subsetInf.ans[child_pt] = ("one", [])
                tfl.append(child_pt)
    elif isinstance(pv2, N):
        nx = N(v1)
        nx.negate(len(database.universe))
        if nx.val == v2:
            for i in database.universe:
                child_pt = (t, v1, i)
                subsetInf.ans[child_pt] = ("zero", [])
                tfl.append(child_pt)
    else:
        my_dict = {}
        if isinstance(pv2, R):
            my_dict[pv1] = v1
            my_dict[pv2.term] = v2
        else:
            my_dict[pv1] = v1
            if pv2 in my_dict:
                if v2 != my_dict[pv2]:
                    child_pt = (t, my_dict['x'], change(verbs[0], v1, verbs))
                    subsetInf.ans[child_pt] = ("down", [])
                    tfl.append(child_pt)


def anti(database, tf, ptf, tfl):
    t, v1, v2 = tf
    pt, pv1, pv2 = ptf
    nx = N(v1)
    ny = N(v2)
    nx.negate(len(database.universe))
    ny.negate(len(database.universe))
    child_pt = (t, ny.val, nx.val)
    subsetInf.ans[child_pt] = ("anti", [])
    tfl.append(child_pt)
    if len(verbs):
        for v in verbs:
            child_pt = (t, change(v, v1, verbs), change(v, v2, verbs))
            subsetInf.ans[child_pt] = ("anti", [])
            tfl.append(child_pt)
