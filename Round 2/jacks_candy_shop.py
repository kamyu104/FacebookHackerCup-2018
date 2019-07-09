# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Jack's Candy Shop
# https://www.facebook.com/hackercup/problem/638251746380051/
#
# Time:  O(N * (logN)^2)
# Space: O(N)
#

from functools import partial
from collections import defaultdict
from heapq import heappush, heappop

def divide(stk, adj, count, max_heaps, i, result):
    stk.append(partial(conquer, count, max_heaps, i, result))
    for j in adj[i]:
        stk.append(partial(merge, max_heaps, i, j))
        stk.append(partial(divide, stk, adj, count, max_heaps, j, result))

def merge(max_heaps, i, j):
    if len(max_heaps[i]) < len(max_heaps[j]):
        max_heaps[i], max_heaps[j] = max_heaps[j], max_heaps[i]
    while max_heaps[j]:
        heappush(max_heaps[i], heappop(max_heaps[j]))
    max_heaps.pop(j)

def conquer(count, max_heaps, i, result):
    heappush(max_heaps[i], -i)
    while count[i] and max_heaps[i]:
        count[i] -= 1
        result[0] += -heappop(max_heaps[i])

def jacks_candy_shop():
    N, M, A, B = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for i in xrange(1, N):
        adj[input()].append(i)
    count = [0]*N
    for i in xrange(M):
        count[(A*i+B) % N] += 1

    result = [0]
    max_heaps = defaultdict(list)
    stk = []
    stk.append(partial(divide, stk, adj, count, max_heaps, 0, result))
    while stk:
        stk.pop()()
    max_heaps.pop(0)
    return result[0]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, jacks_candy_shop())
