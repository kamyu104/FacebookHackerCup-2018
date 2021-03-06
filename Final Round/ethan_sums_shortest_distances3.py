# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - Ethan Sums Shortest Distances
# https://www.facebook.com/hackercup/problem/278591946122939/
#
# Time:  O(N^3), optimized from ethan_sums_shortest_distances2.py
# Space: O(N^2)
#

# dp[r][g]: min. cost from column 1 to column g and where nodes are all connected,
#           and column g is the left node of the gap

def ethan_sums_shortest_distances():
    N = input()
    A = [map(int, raw_input().strip().split()) for _ in xrange(2)]

    accu = [[0 for _ in xrange(N+1)] for _ in xrange(2)]
    for i in xrange(2):  # Time: O(N)
        for j in xrange(N):
            accu[i][j+1] = accu[i][j]+A[i][j]
    S = accu[0][N]+accu[1][N]
    
    partial_accu_from_left = [[[0 for _ in xrange(N+1)] for _ in xrange(N+1)] for _ in xrange(2)]
    full_accu_from_left = [[[0 for _ in xrange(N+1)] for _ in xrange(N+1)] for _ in xrange(2)]
    partial_accu_from_right = [[[0 for _ in xrange(N+1)] for _ in xrange(N+1)] for _ in xrange(2)]
    full_accu_from_right = [[[0 for _ in xrange(N+1)] for _ in xrange(N+1)] for _ in xrange(2)]
    for r in xrange(2):  # Time: O(N^2)
        for g in xrange(1, N+1):
            s = 0
            for c in xrange(g-1, N):
                s += A[r][c]
                partial_accu_from_left[r][g][c+1] = partial_accu_from_left[r][g][c] + s*(S-s)
            s = accu[r][g-1]+accu[r^1][g-1]
            for c in xrange(g-1, N):
                s += A[r][c]
                full_accu_from_left[r][g][c+1] = full_accu_from_left[r][g][c] + s*(S-s)
        for g in reversed(xrange(1, N+1)):
            s = 0
            for c in reversed(xrange(g)):
                s += A[r][c]
                partial_accu_from_right[r][g][c] = partial_accu_from_right[r][g][c+1] + s*(S-s)
            s = (accu[r][N]-accu[r][g])+(accu[r^1][N]-accu[r^1][g])
            full_accu_from_right[r][g][g] = s*(S-s)
            for c in reversed(xrange(g)):
                s += A[r][c]
                full_accu_from_right[r][g][c] = full_accu_from_right[r][g][c+1] + s*(S-s)

    dp = [[float("inf") for _ in xrange(N+1)] for _ in xrange(2)]
    dp[0][0] = dp[1][0] = 0
    for r in xrange(2):  # Time: O(N^3)
        for g in xrange(N):
            for nr in xrange(2):
                for ng in xrange(g+1, N+1):
                    for join in xrange(g, ng):
                        if r == nr:
                            s = accu[r][ng]-accu[r][g]
                            curr = partial_accu_from_left[r][g+1][join] + \
                                   full_accu_from_left[r^1][g+1][join] + \
                                   partial_accu_from_right[r][ng][join+1] + \
                                   full_accu_from_right[r^1][ng][join+1] + \
                                   s*(S-s)
                        else:
                            s = accu[r][g]+accu[r^1][ng]
                            curr = partial_accu_from_left[r][g+1][join] + \
                                   full_accu_from_left[r^1][g+1][join] + \
                                   partial_accu_from_right[r^1][ng][join+1] + \
                                   full_accu_from_right[r][ng][join+1] + \
                                   s*(S-s)
                        dp[nr][ng] = min(dp[nr][ng], dp[r][g] + curr)

    assert(dp[0][N] == dp[1][N])
    return dp[0][N]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_sums_shortest_distances())
