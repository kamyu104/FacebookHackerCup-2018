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

    def __init__(self, nums,
                 query_fn=min,
                 update_fn=lambda x, y: y,
                 default_val=float("inf")):
        N = len(nums)
        self.__original_length = N
        self.__tree_length = 2**(N.bit_length() + (N&(N-1) != 0))-1
        self.__query_fn = query_fn
        self.__update_fn = update_fn
        self.__default_val = default_val
        self.__tree = [default_val for _ in range(self.__tree_length)]
        self.__lazy = [None for _ in range(self.__tree_length)]
        self.__constructTree(nums, 0, self.__original_length-1, 0)

    def update(self, i, val):
        self.__updateTree(val, i, i, 0, self.__original_length-1, 0)

    def query(self, i, j):
        return self.__queryRange(i, j, 0, self.__original_length-1, 0)

    def __constructTree(self, nums, left, right, idx):
        if left > right:
             return
        if left == right:
            self.__tree[idx] = self.__update_fn(self.__tree[idx], nums[left])
            return 
        mid = left + (right-left)//2
        self.__constructTree(nums, left, mid, idx*2 + 1)
        self.__constructTree(nums, mid+1, right, idx*2 + 2)
        self.__tree[idx] = self.__query_fn(self.__tree[idx*2 + 1], self.__tree[idx*2 + 2])

    def __apply(self, left, right, idx, val):
        self.__tree[idx] = self.__update_fn(self.__tree[idx], val)
        if left != right:
            self.__lazy[idx*2 + 1] = self.__update_fn(self.__lazy[idx*2 + 1], val)
            self.__lazy[idx*2 + 2] = self.__update_fn(self.__lazy[idx*2 + 2], val)

    def __updateTree(self, val, range_left, range_right, left, right, idx):
        if left > right:
            return
        if self.__lazy[idx] is not None:
            self.__apply(left, right, idx, self.__lazy[idx])
            self.__lazy[idx] = None
        if range_left > right or range_right < left:
            return
        if range_left <= left and right <= range_right:
            self.__apply(left, right, idx, val)
            return
        mid = left + (right-left)//2
        self.__updateTree(val, range_left, range_right, left, mid, idx*2 + 1)
        self.__updateTree(val, range_left, range_right, mid+1, right, idx*2 + 2)
        self.__tree[idx] = self.__query_fn(self.__tree[idx*2 + 1],
                                           self.__tree[idx*2 + 2])

    def __queryRange(self, range_left, range_right, left, right, idx):
        if left > right:
            return self.__default_val
        if self.__lazy[idx] is not None:
            self.__apply(left, right, idx, self.__lazy[idx])
            self.__lazy[idx] = None
        if right < range_left or left > range_right:
            return self.__default_val
        if range_left <= left and right <= range_right:
            return self.__tree[idx]
        mid = left + (right-left)//2
        return self.__query_fn(self.__queryRange(range_left, range_right, left, mid, idx*2 + 1), 
                               self.__queryRange(range_left, range_right, mid + 1, right, idx*2 + 2))

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
    segment_tree = SegmentTree([float("inf")]*N)
    for i in xrange(N):
        while max_D and P[max_D[0]]+2*M < P[i]:
            max_D.popleft()
        while P[j]+2*M < P[i]:
            j += 1
        if not max_D:
            dp[i+1] = dp[i]+S+D[i]
            max_D.append(i)
        else:
            while max_D and D[max_D[-1]] <= D[i]:  # keep descending
                r = max_D.pop()
                segment_tree.update(r, float("inf"))
            if max_D:
                segment_tree.update(i, dp[max_D[-1]+1]+S+D[i])
            max_D.append(i)
            dp[i+1] = min(dp[(j-1)+1]+S+D[max_D[0]],
                          segment_tree.query(max_D[0]+1, i))
    return dp[N]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, fossil_fuels())
