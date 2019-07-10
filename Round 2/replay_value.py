
# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Replay Value
# https://www.facebook.com/hackercup/problem/271442536778669/
#
# Time:  O(N^5)
# Space: O(N^4)
#

def replay_value():
    N, S, E = map(int, raw_input().strip().split())
    emitters = [list(map(int, raw_input().strip().split())) for _ in xrange(N)]

    emitters.extend([[float("inf"), S], [float("inf"), E]])
    emitters.sort(key=lambda x : x[1])
    for i, emitter in enumerate(emitters):  # compress Y
        if emitter[1] == S:
            S = i
        elif emitter[1] == E:
            E = i
        emitter[1] = i
    if S < E:  # make S higher than E
        S = N+1 - S
        E = N+1 - E
        for emitter in emitters:  # mirror Y
            emitter[1] = N+1 - emitter[1]
    emitters.sort(), emitters.pop(), emitters.pop()

    dp = [[[[[0 for _ in xrange(N+2)] for _ in xrange(N+2)] for _ in xrange(N+2)] for _ in xrange(N+2)] for _ in xrange(2)]
    dp[-1][N+1][0][N+1][0] = 1
    for i, (x, y) in enumerate(emitters):
        dp[i%2] = [[[[0 for _ in xrange(N+2)] for _ in xrange(N+2)] for _ in xrange(N+2)] for _ in xrange(N+2)]
        for a in xrange(N+2):  # lowest up
            for b in xrange(N+2):  # highest down
                for c in xrange(N+2):  # lowest right higher than E
                    for d in xrange(N+2):  # hight right lower then E
                        v = dp[(i-1)%2][a][b][c][d]
                        if not v:
                            continue
                        if not (y < d):  # up
                            dp[i%2][min(a, y)][b][c][d] = (dp[i%2][min(a, y)][b][c][d]+v) % MOD
                        if not (y > c):  # down
                            dp[i%2][a][max(b, y)][c][d] = (dp[i%2][a][max(b, y)][c][d]+v) % MOD
                        if not (a < y < S or S < y < b):  # left
                            dp[i%2][a][b][c][d] = (dp[i%2][a][b][c][d]+v) % MOD
                        if y > E:  # right
                            dp[i%2][a][b][min(c, y)][d] = (dp[i%2][a][b][min(c, y)][d]+v) % MOD
                        else:
                            dp[i%2][a][b][c][max(d, y)] = (dp[i%2][a][b][c][max(d, y)]+v) % MOD
    result = pow(4, N, MOD)
    for a in xrange(N+2):
        for b in xrange(N+2):
            for c in xrange(N+2):
                for d in xrange(N+2):
                    result = (result-dp[(N-1)%2][a][b][c][d]) % MOD
    return result

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, replay_value())
