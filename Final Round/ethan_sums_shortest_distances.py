# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - Ethan Sums Shortest Distances
# https://www.facebook.com/hackercup/problem/278591946122939/
#
# Time:  O(N^4)
# Space: O(N^2)
#

# based on official solution:
# dp[i][r][g] = min. cost such that:
# - you're ending at a vertical edge in column i (its cost is exluded)
# - you previously had a partial horizontal section in row r (r = 2 indicates both rows)
# - the partial horizontal section started in column g

def ethan_sums_shortest_distances():
    N = input()
    A = [map(int, raw_input().strip().split()) for _ in xrange(2)]

    accu = [[0 for _ in xrange(N+1)] for _ in xrange(2)]
    for i in xrange(2):  # Time: O(N)
        for j in xrange(N):
            accu[i][j+1] = accu[i][j]+A[i][j]

    S = accu[0][N]+accu[1][N]
    dp = [[[float("inf") for _ in xrange(N)] for _ in xrange(3)] for _ in xrange(N)]
    for i in xrange(N):  # Time: O(N^2)
        dp[i][2][0] = 0
        for j in xrange(2):
            s = 0
            for k in xrange(i):
                s += A[j][k]
                dp[i][2][0] += s*(S-s)

    for i in xrange(N):  # Time: O(N^4)
        for ni in xrange(i+1, N):
            for nr in xrange(2):
                for ng in xrange(i+1, ni+1):
                    curr = 0
                    s = accu[nr][ng]+accu[nr^1][i]
                    for j in xrange(i, ni):
                        s += A[nr^1][j]
                        curr += s*(S-s)
                    s = 0
                    for j in reversed(xrange(i+1, ng)):
                        s += A[nr][j]
                        curr += s*(S-s)
                    s = 0
                    for j in xrange(ng, ni):
                        s += A[nr][j]
                        curr += s*(S-s)
                    for r in xrange(3):
                        for g in xrange(i+1):
                            if r == 2:
                                s = accu[nr][ng]
                            else:
                                s = accu[nr][ng]-accu[nr][g] if (r == nr) else accu[nr][ng]+accu[nr^1][g]
                            dp[ni][nr][ng] = min(dp[ni][nr][ng], dp[i][r][g] + s*(S-s) + curr)

    result = float("inf")
    for i in xrange(N):  # Time: O(N^3)
        for r in xrange(3):
            for g in xrange(i+1):
                curr = 0
                for j in xrange(2):
                    s = 0
                    for k in reversed(xrange(i+1, N)):
                        s += A[j][k]
                        curr += s*(S-s)
                s = accu[0][N] if (r == 2) else accu[r][N]-accu[r][g]
                result = min(result, dp[i][r][g] + s*(S-s) + curr)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_sums_shortest_distances())
