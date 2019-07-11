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
    
    def __init__(self, N):
        self.N = N
        self.st = [float("inf") for i in range(0,4*N)] # approximate the overall size of segment tree with array N
        self.lazy = [0 for i in range(0,4*N)] # create array to store lazy update
        self.flag = [0 for i in range(0,4*N)] # flag for lazy update
        
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
            self.st[idx] = min(self.st[self.left(idx)] , self.st[self.right(idx)])

    # update with O(logN) (Normal segment tree without lazy update will take O(NlogN) for each update)
    def update(self, idx, l, r, a, b, val): # update(1, 1, N, a, b, v) for update val v to [a,b]
        a, b = a+1, b+1
        if self.flag[idx] == True:
            self.st[idx] = self.lazy[idx]
            self.flag[idx] = False
            if l!=r:
                self.lazy[self.left(idx)] = self.lazy[idx]
                self.lazy[self.right(idx)] = self.lazy[idx]
                self.flag[self.left(idx)] = True
                self.flag[self.right(idx)] = True
            
        if r < a or l > b:
            return True
        if l >= a and r <= b :
            self.st[idx] = val
            if l!=r:
                self.lazy[self.left(idx)] = val
                self.lazy[self.right(idx)] = val
                self.flag[self.left(idx)] = True
                self.flag[self.right(idx)] = True
            return True
        mid = (l+r)//2
        self.update(self.left(idx),l,mid,a,b,val)
        self.update(self.right(idx),mid+1,r,a,b,val)
        self.st[idx] = min(self.st[self.left(idx)] , self.st[self.right(idx)])
        return True

    # query with O(lg N)
    def query(self, idx, l, r, a, b): # query(1, 1, N, a, b) for query min of [a,b]
        a, b = a+1, b+1
        if self.flag[idx] == True:
            self.st[idx] = self.lazy[idx]
            self.flag[idx] = False
            if l != r:
                self.lazy[self.left(idx)] = self.lazy[idx]
                self.lazy[self.right(idx)] = self.lazy[idx]
                self.flag[self.left(idx)] = True
                self.flag[self.right(idx)] = True
        if r < a or l > b:
            return float("inf")
        if l >= a and r <= b:
            return self.st[idx]
        mid = (l+r)//2
        q1 = self.query(self.left(idx),l,mid,a,b)
        q2 = self.query(self.right(idx),mid+1,r,a,b)
        return min(q1,q2)

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
                segment_tree.update(1, 1, N, r, r, float("inf"))
            if max_D:
                segment_tree.update(1, 1, N, i, i, dp[max_D[-1]+1] + S + D[i])
            max_D.append(i)
            dp[i+1] = min(dp[(j-1)+1] + S + D[max_D[0]],
                          segment_tree.query(1, 1, N, max_D[0]+1, i))
    return dp[N]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, fossil_fuels())
