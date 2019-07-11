# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Fossil Fuels
# https://www.facebook.com/hackercup/problem/469838700128124/
#
# Time:  O(NlogN)
# Space: O(N)
#

from collections import deque

# reference: https://github.com/TheAlgorithms/Python/blob/05e5172093dbd0633ce83044603073dd2be675c4/data_structures/binary_tree/lazy_segment_tree.py
class SegmentTree(object):
    
    def __init__(self, N, query_fn=min, default_val=float("inf")):
        self.N = N
        self.query_fn = query_fn
        self.default_val = default_val
        self.st = [default_val for i in range(0,4*N)] # approximate the overall size of segment tree with array N
        self.lazy = [None for i in range(0,4*N)] # create array to store lazy update
        
    def left(self, idx):
        return idx*2

    def right(self, idx):
        return idx*2 + 1

    def build(self, idx, l, r, A):
        if l==r:
            self.st[idx] = A[l-1]
        else :
            mid = (l+r)//2
            self.build(self.left(idx),l,mid, A)
            self.build(self.right(idx),mid+1,r, A)
            self.st[idx] = self.default_val(self.st[self.left(idx)] , self.st[self.right(idx)])

    # update with O(logN) (Normal segment tree without lazy update will take O(NlogN) for each update)
    def update(self, a, b, val, idx=1, l=1, r=None): # update(a, b, v) for update val v to [a,b]
        if r is None:
            r = self.N
        if self.lazy[idx] is not None:
            self.st[idx] = self.lazy[idx]
            if l!=r:
                self.lazy[self.left(idx)] = self.lazy[idx]
                self.lazy[self.right(idx)] = self.lazy[idx]
            self.lazy[idx] = None
            
        if r < a or l > b:
            return
        if l >= a and r <= b :
            self.st[idx] = val
            if l!=r:
                self.lazy[self.left(idx)] = val
                self.lazy[self.right(idx)] = val
            return
        mid = (l+r)//2
        self.update(a,b,val,self.left(idx),l,mid)
        self.update(a,b,val,self.right(idx),mid+1,r)
        self.st[idx] = self.query_fn(self.st[self.left(idx)] , self.st[self.right(idx)])

    # query with O(logN)
    def query(self, a, b, idx=1, l=1, r=None): # query(a, b) for query_fn of [a,b]
        if r is None:
            r = self.N
        if self.lazy[idx] is not None:
            self.st[idx] = self.lazy[idx]
            if l != r:
                self.lazy[self.left(idx)] = self.lazy[idx]
                self.lazy[self.right(idx)] = self.lazy[idx]
        if r < a or l > b:
            return self.default_val
        if l >= a and r <= b:
            return self.st[idx]
        mid = (l+r)//2
        q1 = self.query(a,b,self.left(idx),l,mid)
        q2 = self.query(a,b,self.right(idx),mid+1,r)
        return self.query_fn(q1,q2)
    
    def showData(self):
        showList = []
        for i in xrange(1,self.N+1):
            showList += [self.query(i, i, 1, 1, self.N)]
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
                segment_tree.update(r+1, r+1, float("inf"))
            if max_D:
                segment_tree.update(i+1, i+1, dp[max_D[-1]+1] + S + D[i])
            max_D.append(i)
            dp[i+1] = min(dp[(j-1)+1] + S + D[max_D[0]],
                          segment_tree.query((max_D[0]+1)+1, i+1))
    return dp[N]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, fossil_fuels())
