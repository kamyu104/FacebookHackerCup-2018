# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Jack's Candy Shop
# https://www.facebook.com/hackercup/problem/638251746380051/
#
# Time:  O(N * (logN)^2)
# Space: O(N)
#

from sys import setrecursionlimit
from heapq import heappush, heappop

def jacks_candy_shop_helper(adj, i, count):
    result = 0
    max_heap = []
    for j in adj[i]:
        curr_max, remain = jacks_candy_shop_helper(adj, j, count)
        result += curr_max
        if len(max_heap) > len(remain):
            max_heap, remain = remain, max_heap
        while remain:
            heappush(max_heap, heappop(remain))

    heappush(max_heap, -i)
    while count[i] and max_heap:
        count[i] -= 1
        result += -heappop(max_heap)
    return result, max_heap

def jacks_candy_shop():
    N, M, A, B = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for i in xrange(1, N):
        adj[input()].append(i)
    count = [0]*N
    for i in xrange(M):
        count[(A*i+B) % N] += 1
    
    return jacks_candy_shop_helper(adj, 0, count)[0]

setrecursionlimit(200000)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, jacks_candy_shop())
