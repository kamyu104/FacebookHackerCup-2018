# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - Stockholm
# https://www.facebook.com/hackercup/problem/2019100985085971/
#
# Time:  O(logA + logB)
# Space: O(logA + logB)
#

def binary_string(x):
    result = []
    while x:
        result.append(x%2)
        x //= 2
    return result[::-1]

def LCA(x, y):
    for i in xrange(min(len(x), len(y))):
        if x[i] != y[i]:
            return i
    return i+1

def distance(x):
    result, l, has_outer_island = 0, len(x), False
    while l:
        i = l-1
        while i and x[i] == x[i-1]:
            i -= 1
        if i:
            i -= 1
        if not i:
            has_outer_island = (l >= 2 and x[0] == x[l-1])
            break
        l = i
        result += 1
    return result, has_outer_island

def contest_environment():
    A, B = map(int, raw_input().strip().split())
    X, Y = binary_string(A+1), binary_string(B+1)
    lca = LCA(X, Y)
    X, Y = X[lca:] if lca < len(X) else [], Y[lca:] if lca < len(Y) else []
    dist1, dist2 = distance(X), distance(Y)
    return dist1[0]+dist2[0]+int(len(X) and len(Y) and (dist1[1] or dist2[1]))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, contest_environment())
