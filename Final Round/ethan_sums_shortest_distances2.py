# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - Ethan Sums Shortest Distances
# https://www.facebook.com/hackercup/problem/278591946122939/
#
# Time:  O(N^4)
# Space: O(N)
#

# dp[r][g]: min. cost from column 1 to column g and where nodes are all connected,
#           and column g is the left node of the gap

def ethan_sums_shortest_distances():
    N = input()
    A = [map(int, raw_input().strip().split()) for _ in xrange(2)]
    S = sum(A[0])+sum(A[1])

    dp = [[float("inf") for _ in xrange(N+1)] for _ in xrange(2)]
    dp[0][0] = dp[1][0] = 0
    for r in xrange(2):
        for g in xrange(N):
            for nr in xrange(2):
                for ng in xrange(g+1, N+1):
                    for join in xrange(g, ng):
                        curr = 0
                        if r == nr:
                            s = 0
                            for c in xrange(g, join):
                                s += A[r][c]
                                curr += s*(S-s)
                            s = 0
                            for c in reversed(xrange(join+1, ng)):
                                s += A[r][c]
                                curr += s*(S-s)
                            s = 0
                            for c in xrange(g, ng):
                                s += A[r][c]
                            curr += s*(S-s)
                            s = 0
                            for c in xrange(g):
                                s += A[r][c] + A[r^1][c]
                            for c in xrange(g, join):
                                s += A[r^1][c]
                                curr += s*(S-s)
                            for c in xrange(g, ng):
                                s += A[r][c]
                            for c in xrange(join, ng):
                                s += A[r^1][c]
                                curr += s*(S-s)
                        else:
                            s = 0
                            for c in xrange(g, join):
                                s += A[r][c]
                                curr += s*(S-s)
                            s = 0
                            for c in reversed(xrange(join+1, ng)):
                                s += A[nr][c]
                                curr += s*(S-s)
                            s = 0
                            for c in xrange(g):
                                s += A[r][c] + A[r^1][c]
                            for c in xrange(g, join):
                                s += A[nr][c]
                                curr += s*(S-s)
                            for c in xrange(join, ng):
                                s += A[nr][c]
                            curr += s*(S-s)
                            for c in xrange(g, join):
                                s += A[r][c]
                            for c in xrange(join, ng):
                                s += A[r][c]
                                curr += s*(S-s)
                        dp[nr][ng] = min(dp[nr][ng], dp[r][g]+curr)

    assert(dp[0][N] == dp[1][N])
    return dp[0][N]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_sums_shortest_distances())
