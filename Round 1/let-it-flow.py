# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 1 - Let It Flow
# https://www.facebook.com/hackercup/problem/180494849326631/
#
# Time:  O(N)
# Space: O(W), W is the number of walls
#

M = 1000000007

def let_it_flow():
    N = input()
    lookup = set()
    for j in xrange(3):
        for i, c in enumerate(raw_input().strip()):
             if c == '#':
                lookup.add((i, j))
    dp = [[0 for _ in xrange(3)] for _ in xrange(2)]
    dp[0][1] = 1 if (0, 0) not in lookup and (0, 1) not in lookup else 0
    for i in xrange(1, N):
        dp[i%2][0] = dp[(i-1)%2][1] if (i, 1) not in lookup and (i, 0) not in lookup else 0
        dp[i%2][1] = dp[(i-1)%2][0] if (i, 0) not in lookup and (i, 1) not in lookup else 0
        dp[i%2][1] = (dp[i%2][1]+dp[(i-1)%2][2])%M if (i, 2) not in lookup and (i, 1) not in lookup else dp[i%2][1]
        dp[i%2][2] = dp[(i-1)%2][1] if (i, 1) not in lookup and (i, 2) not in lookup else 0
    return dp[(N-1)%2][2]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, let_it_flow())
