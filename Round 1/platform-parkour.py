# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 1 - Platform Parkour
# https://www.facebook.com/hackercup/problem/1892930427431211/
#
# Time:  O(N * (M + logZ))
# Space: O(N)
#

EPS = 1e-6

def check(N, H, U, D, x):  # Time: O(N)
    down, up = H[0]-x, H[0]+x
    for i in xrange(N-1):
        down, up = max(down-D[i], H[i+1]-x), min(up+U[i], H[i+1]+x)
        if down > up:
            return False
    return True

def platform_parkour():
    N, M = map(int, raw_input().strip().split())
    H = [0]*N
    H[0], H[1], W, X, Y, Z = map(int, raw_input().strip().split())
    for i in xrange(2, N):
        H[i] =(W*H[i-2]+X*H[i-1]+Y)%Z

    # Time:  O(N*M)
    U, D = [float("inf")]*N, [float("inf")]*N
    for i in xrange(M):
        a, b, u, d = map(int, raw_input().strip().split())
        a -= 1
        b -= 1
        if a > b:
            a, b = b, a
            u, d = d, u
        for j in xrange(a, b):
            U[j] = min(U[j], u)
            D[j] = min(D[j], d)

    # Time:  O(NlogZ)
    left, right = 0.0, float(max(H)-min(H))
    while left+EPS < right:
        mid = left + (right-left)/2
        if check(N, H, U, D, mid):
            right = mid
        else:
            left = mid
    return left

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, platform_parkour())
