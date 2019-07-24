# Copyright (c) 2019 kamyu. Al rights reserved.
#
# Facebook Hacker Cup 2019 Round 3 - Finshakes
# https://www.facebook.com/hackercup/problem/206776773482750/
#
# Time:  O(M^3)
# Space: O(M^2)
#

def f(x):
    return x*(x-1)//2

def finshakes():
    N, M, W = map(int, raw_input().strip().split())
    H = map(int, raw_input().strip().split())
    H.insert(0, 0)

    intervals = []
    endpoint_set = set()
    for i in xrange(M):
        P, J = map(int, raw_input().strip().split())
        l, r = P, P
        while l > 1 and H[l]+J > W:
            l -= 1
        while r < N and H[r]+J > W:
            r += 1
        intervals.append([l, r])
        endpoint_set.add(l)
        endpoint_set.add(r)
    lookup = {v:k for k, v in enumerate(sorted(endpoint_set), 1)}
    for interval in intervals:  # compress intervals
        interval[L] = lookup[interval[L]]
        interval[R] = lookup[interval[R]]

    M2 = len(endpoint_set)
    dp = [[0 for _ in xrange(M2+1)] for _ in xrange(M2+2)]
    for l in xrange(M2):
        for i in xrange(M2-l+1):
            j = i+l
            C = [0]*(M2+2)
            for interval in intervals:
                if i <= interval[L] and interval[R] <= j:
                    C[interval[L]] += 1
                    C[interval[R]+1] -= 1
            for m in xrange(i, j+1):
                C[m+1] += C[m]
            if l == 0:
                dp[i][j] = f(C[i])
            else:
                for m in xrange(i, j+1):
                    dp[i][j] = max(dp[i][j], dp[i][m-1] + f(C[m]) + dp[m+1][j])
    return dp[1][M2]

L, R = range(2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, finshakes())
