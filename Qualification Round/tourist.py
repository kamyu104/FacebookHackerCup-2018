# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Qualification Round - Tourist
# https://www.facebook.com/hackercup/problem/1632703893518337/
#
# Time:  O(K)
# Space: O(1)
#

import fractions
import itertools

def tourist():
    N, K, V = map(int, raw_input().strip().split())
    A = []
    for i in xrange(N):
        A.append(raw_input().strip())

    cycle = N // fractions.gcd(N, K)
    count = V % cycle if V % cycle else cycle
    start = (count-1) * K % N
    return " ".join([A[i] for i in itertools.chain(xrange(max(0, start+K-N)),
                                                   xrange(start, min(N, start+K)))])

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, tourist())
