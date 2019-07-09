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

def jacks_candy_shop_helper(adj, i, C, max_heaps, result):
    for j in xrange(len(adj[i])):
        jacks_candy_shop_helper(adj, j, C, max_heaps, result)
        if len(max_heaps[i]) > len(max_heaps[j]):
            max_heaps[i], max_heaps[j] = max_heaps[j], max_heaps[i]
        while max_heaps[j]:
            heappush(max_heaps[i], heappop(max_heaps[j]))

    heappush(max_heaps[i], -i)
    while C[i] and max_heaps[i]:
        C[i] -= 1
        result[0] += -heappop(max_heaps[i])

def jacks_candy_shop():
    N, M, A, B = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for i in xrange(1, N):
        p = input()
        adj[p].append(i)
    C = [0]*N
    for i in xrange(M):
        C[(A*i+B) % N] += 1
    
    result = [0]
    max_heaps = [[] for _ in xrange(N)]
    jacks_candy_shop_helper(adj, 0, C, max_heaps, result)
    return result[0]

setrecursionlimit(200000)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, jacks_candy_shop())
