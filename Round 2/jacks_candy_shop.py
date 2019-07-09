# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Jack's Candy Shop
# https://www.facebook.com/hackercup/problem/638251746380051/
#
# Time:  O(N * (logN)^2)
# Space: O(N)
#

from heapq import heappush, heappop

def jacks_candy_shop():
    N, M, A, B = map(int, raw_input().strip().split())
    adj = [[] for _ in xrange(N)]
    for i in xrange(1, N):
        adj[input()].append(i)
    count = [0]*N
    for i in xrange(M):
        count[(A*i+B) % N] += 1

    result = 0
    max_heaps = [[] for _ in xrange(N)]
    stk = [(0, (0))]
    while stk:
        step, args = stk.pop()
        if step == 0:
            i = args
            stk.append((2, (i)))
            for j in adj[i]:
                stk.append((1, (i, j)))
                stk.append((0, (j)))
        elif step == 1:
            i, j = args
            if len(max_heaps[i]) > len(max_heaps[j]):
                max_heaps[i], max_heaps[j] = max_heaps[j], max_heaps[i]
            while max_heaps[j]:
                heappush(max_heaps[i], heappop(max_heaps[j]))
        else:
            i = args
            heappush(max_heaps[i], -i)
            while count[i] and max_heaps[i]:
                count[i] -= 1
                result += -heappop(max_heaps[i])
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, jacks_candy_shop())
