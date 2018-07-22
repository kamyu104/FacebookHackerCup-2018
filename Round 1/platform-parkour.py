# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 1 - Platform Parkour
# https://www.facebook.com/hackercup/problem/1892930427431211/
#
# Time:  O(N*M), could be improved to O(NlogZ + M)
# Space: O(N)
#

EPS = 1e-6
def check(N, H, U, D, x):
    a = H[0]-x
    b = H[0]+x
    for i in xrange(N-1):
        a = max(a-D[i], H[i+1]-x)
        b = min(b+U[i], H[i+1]+x)
        if a > b:
            return False
    return True

def platform_parkour():
    N, M = map(int, raw_input().strip().split())
    H = [0]*N
    H[0], H[1], W, X, Y, Z = map(int, raw_input().strip().split())
    for i in xrange(2, N):
        H[i] =(W*H[i-2]+X*H[i-1]+Y)%Z
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

    left, right = 0.0, 10e6
    while left+EPS < right:
        mid = left + (right-left)/2
        if check(N, H, U, D, mid):
            right = mid
        else:
            left = mid
    return left

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, platform_parkour())
