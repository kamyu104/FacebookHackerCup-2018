# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Fossil Fuels
# https://www.facebook.com/hackercup/problem/469838700128124/
#
# Time:  O(NlogN)
# Space: O(N)
#

from collections import deque

class SegmentTree(object):
    def __init__(self, N,
                 query_fn=min,
                 update_fn=lambda x, y: y,
                 default_val=float("inf")):
        self.N = N
        self.H = (N-1).bit_length()
        self.query_fn = lambda x, y: query_fn(x, y) if x is not None else y
        self.update_fn = update_fn
        self.default_val = default_val
        self.tree = [default_val] * (2 * N)
        self.lazy = [None] * N

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
            self.lazy[x] = self.query_fn(self.lazy[x], val)

    def __pull(self, x):
        while x > 1:
            x //= 2
            self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2 + 1])
            if self.lazy[x] is not None:
                self.tree[x] = self.query_fn(self.tree[x], self.lazy[x])

    def __push(self, x):
        n = 2**self.H
        while n != 1:
            y = x // n
            if self.lazy[y] is not None:
                self.__apply(y*2, self.lazy[y])
                self.__apply(y*2 + 1, self.lazy[y])
                self.lazy[y] = None
            n //= 2

    def update(self, L, R, h):
        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:
                self.__apply(L, h)
                L += 1
            if R & 1 == 0:
                self.__apply(R, h)
                R -= 1
            L //= 2
            R //= 2
        self.__pull(L0)
        self.__pull(R0)

    def query(self, L, R):
        result = self.default_val
        if L > R:
            return result

        L += self.N
        R += self.N
        self.__push(L)
        self.__push(R)
        while L <= R:
            if L & 1:
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L //= 2
            R //= 2
        return result
    
    def showData(self):
        showList = []
        for i in xrange(self.N):
            showList += [self.query(i, i)]
        print (showList)

def fossil_fuels():
    N, S, M, K = map(int, raw_input().strip().split())
    P = []
    for i in xrange(K):
        L, A, X, Y, Z = map(int, raw_input().strip().split())
        for j in xrange(L):
            P.append(A)
            A=(X*A+Y)%Z+1
    D = []
    for i in xrange(K):
        L, A, X, Y, Z = map(int, raw_input().strip().split())
        for j in xrange(L):
            D.append(A)
            A=(X*A+Y)%Z+1
    PD = zip(P, D)
    PD.sort()
    P, D = [x[0] for x in PD], [x[1] for x in PD]

    dp = [0]*(N+1)
    max_D = deque()
    j = 0
    segment_tree = SegmentTree(N)
    for i in xrange(N):
        while max_D and P[max_D[0]] + 2*M < P[i]:
            max_D.popleft()
        while P[j] + 2*M < P[i]:
            j += 1
        if not max_D:
            dp[i+1] = dp[i] + S + D[i]
            max_D.append(i)
        else:
            while max_D and D[max_D[-1]] <= D[i]:  # keep descending
                r = max_D.pop()
                segment_tree.update(r, r, float("inf"))
            if max_D:
                segment_tree.update(i, i, dp[max_D[-1]+1] + S + D[i])
            max_D.append(i)
            dp[i+1] = min(dp[(j-1)+1] + S + D[max_D[0]],
                          segment_tree.query(max_D[0]+1, i))
    return dp[N]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, fossil_fuels())
