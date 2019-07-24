# Copyright (c) 2019 kamyu. Al rights reserved.
#
# Facebook Hacker Cup 2019 Round 3 - Finshakes
# https://www.facebook.com/hackercup/problem/206776773482750/
#
# Time:  O(N^2 * M)
# Space: O(N^2)
#

def f(x):
    return x*(x-1)//2

def finshakes():
    N, M, W = map(int, raw_input().strip().split())
    H = map(int, raw_input().strip().split())
    H.insert(0, 0)

    intervals = []
    for i in xrange(M):
        P, J = map(int, raw_input().strip().split())
        l, r = P, P
        while l > 1 and H[l]+J > W:
            l -= 1
        while r < N and H[r]+J > W:
            r += 1
        intervals.append((l, r, 1))

    dp = [[0 for _ in xrange(N+1)] for _ in xrange(N+2)]
    for l in xrange(N):
        for i in xrange(N-l+1):
            j = i+l
            C = [0]*(N+2)
            for interval in intervals:
                if i <= interval[L] and interval[R] <= j:
                    C[interval[L]] += interval[V]
                    C[interval[R]+1] -= interval[V]
            for m in xrange(i, j+1):
                C[m+1] += C[m]
            if l == 0:
                dp[i][j] = f(C[i])
            else:
                for m in xrange(i, j+1):
                    dp[i][j] = max(dp[i][j], dp[i][m-1] + f(C[m]) + dp[m+1][j])
    return dp[1][-1]

L, R, V = range(3)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, finshakes())
