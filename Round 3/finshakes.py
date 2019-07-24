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
            C = [0]*(l+2)
            for k in xrange(M):
                if intervals[k][L] >= i and intervals[k][R] <= j:
                    C[intervals[k][L]-i] += intervals[k][V]
                    C[intervals[k][R]+1-i] -= intervals[k][V]
            for k in xrange(l+1):
                C[k+1] += C[k]
            if l == 0:
                dp[i][j] = f(C[0])
            else:
                for k in xrange(l+1):
                    dp[i][j] = max(dp[i][j], dp[i][i+k-1] + f(C[k]) + dp[i+k+1][j])
    return dp[1][N]

L, R, V = range(3)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, finshakes())
