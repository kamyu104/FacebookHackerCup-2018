# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - The Claw
# https://www.facebook.com/hackercup/problem/278597692763175/
#
# Time:  O(NlogN)
# Space: O(N)
#

from collections import defaultdict
from bisect import bisect_left

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/little_boat_on_the_sea.py
class SegmentTree(object):
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=max,
                 update_fn=lambda x, y: y if x is None else x+y,
                 default_val=0):
        self.N = N
        self.H = (N-1).bit_length()
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.default_val = default_val
        self.tree = build_fn(N, default_val)
        self.lazy = [None]*N

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
            self.lazy[x] = self.update_fn(self.lazy[x], val)

    def update(self, L, R, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])
                if self.lazy[x] is not None:
                    self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])
        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:  # is right child
                self.__apply(L, h)
                L += 1
            if R & 1 == 0:  # is left child
                self.__apply(R, h)
                R -= 1
            L //= 2
            R //= 2
        pull(L0)
        pull(R0)

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        def push(x):
            n = 2**self.H
            while n != 1:
                y = x // n
                if self.lazy[y] is not None:
                    self.__apply(y*2, self.lazy[y])
                    self.__apply(y*2 + 1, self.lazy[y])
                    self.lazy[y] = None
                n //= 2

        result = self.default_val
        if L > R:
            return result

        L += self.N
        R += self.N
        push(L)
        push(R)
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L //= 2
            R //= 2
        return result
    
    def __str__(self):
        showList = []
        for i in xrange(self.N):
            showList.append(self.query(i, i))
        return ",".join(map(str, showList))

def the_claw():
    N, M = map(int, raw_input().strip().split())
    P, R = [None]*N, [None]*(N-1)
    P_Y, R_Y = defaultdict(list), defaultdict(list)
    result = M
    for i in xrange(N):
        P[i] = tuple(map(int, raw_input().strip().split()))
        result -= P[i][1]
        P_Y[P[i][1]].append(P[i][0])
        if i:
            R[i-1] = (max(P[i-1][0], P[i][0]), min(P[i-1][0],P[i][0]))

    P.sort(), R.sort()
    j, descending_stk = 0, []
    for i in xrange(len(R)):
        while j < len(P) and P[j][0] <= R[i][0]:
            while descending_stk and descending_stk[-1][1] <= P[j][1]:
                descending_stk.pop()
            descending_stk.append(P[j])
            j += 1
        y = descending_stk[bisect_left(descending_stk, (R[i][1], 0))][1]
        result += y+1
        R_Y[y].append(R[i])

    for i in P_Y.iterkeys():
        P_Y[i].sort(), R_Y[i].sort()
        segment_tree = SegmentTree(len(P_Y[i])+1)
        k, dp = 0, -1
        for j in xrange(len(P_Y[i])+1):
            while k < len(R_Y[i]) and \
                  R_Y[i][k][0] < (float("inf") if j == len(P_Y[i]) else P_Y[i][j]):
                segment_tree.update(0, bisect_left(P_Y[i], R_Y[i][k][1]), 1)
                k += 1
            dp = max(dp+1, segment_tree.query(0, len(P_Y[i])))
            segment_tree.update(j, j, dp)
        result -= dp

    return 2*result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, the_claw())
