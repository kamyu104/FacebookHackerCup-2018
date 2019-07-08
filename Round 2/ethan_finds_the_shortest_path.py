# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Ethan Finds the Shortest Path
# https://www.facebook.com/hackercup/problem/988017871357549/
#
# Time:  O(N)
# Space: O(1)
#

def ethan_finds_the_shortest_path():
    N, K = map(int, raw_input().strip().split())

    result = []
    diff = K if N >= 3 and K >= 3 else 0
    result.append((1, N, K))
    K -= 1
    if diff:
        for i in xrange(2, N):
            diff -= K
            result.append((i-1, i, K))
            K -= 1
            if K == 1 or i == N-1:
                diff -= K
                result.append((i, N, K))
                break
    return "\n".join([str(abs(diff)), str(len(result))] +
                     map(lambda x : "%d %d %d" % x, result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_finds_the_shortest_path())

