# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - Stockholm
# https://www.facebook.com/hackercup/problem/2019100985085971/
#
# Time:  O(logA + logB)
# Space: O(logA + logB)
#

def lca(x, y):
    for i in xrange(min(len(x), len(y))):
        if x[i] != y[i]:
            return i
    return i+1

def distance(x):
    dist, l, is_over_lca_bridge = 0, len(x), False
    while l:
        i = l-1
        while i and x[i] == x[i-1]:
            i -= 1
        if i:
            i -= 1
        if not i:
            is_over_lca_bridge = (l >= 2 and x[0] == x[l-1])
            break
        l = i
        dist += 1
    return dist, is_over_lca_bridge

def contest_environment():
    A, B = map(int, raw_input().strip().split())
    X, Y = map(lambda x: "{0:b}".format(x), [A+1, B+1])
    p = lca(X, Y)
    X, Y = map(lambda x: x[p:] if p < len(x) else [], [X, Y])
    dist1, dist2 = map(distance, [X, Y])
    return dist1[0]+dist2[0]+int(len(X) and len(Y) and (dist1[1] or dist2[1]))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, contest_environment())
