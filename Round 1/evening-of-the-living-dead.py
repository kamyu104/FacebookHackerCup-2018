# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 1 - Evening of the Living Dead
# https:#www.facebook.com/hackercup/problem/359971574540051/
#
# Time:  O(N * M)
# Space: O(N)
#

import bisect

M = 1000000007

def inv(x):
    return pow(x, M-2, M)

def add(a, b):
    return (a+b)%M
 
def sub(a, b):
    return (a-b)%M
 
def mult(a, b):
    return (a*b)%M
 
def div(a, b):
    return mult(a, inv(b))

def prob(A, B, i, a, b):
    a = max(a, A[i])
    b = min(b, B[i])
    if a > b:
        return 0
    return div(b-a+1, B[i]-A[i]+1)

def evening_of_the_living_dead():
    N, M = map(int, raw_input().strip().split())
    A, B = [None]*(N-1), [None]*(N-1)
    for i in xrange(N-1):
        A[i], B[i] = map(int, raw_input().strip().split())
    Y = [0]*N
    for _ in xrange(M):
        i, h = map(int, raw_input().strip().split())
        Y[i-1] = max(Y[i-1], h)
    H = sorted(list(set([0, float("inf")] + [h for h in Y if h])))
    for i in xrange(len(Y)):
        # normalized height to 0, 1, 2, ..., len(H)
        Y[i] = bisect.bisect_left(H, Y[i])
    dp_safe = [[0 for _ in xrange(len(H))] for _ in xrange(2)]
    dp_zombie = [[0 for _ in xrange(len(H))] for _ in xrange(2)]
    if Y[0]:
        dp_zombie[1][Y[0]] = 1
    else:
        dp_safe[1][0] = 1
    for i in xrange(1, N):
        z = Y[i]
        accu = [0]*(len(H)+1)
        dp_safe[(i+1)%2] = [0 for _ in xrange(len(H))]
        dp_zombie[(i+1)%2] = [0 for _ in xrange(len(H))]
        for h in xrange(len(H)):
            if dp_zombie[i%2][h]:
                if z >= h:  # new zombie's at least as tall
                    dp_zombie[(i+1)%2][z] = add(dp_zombie[(i+1)%2][z], dp_zombie[i%2][h])
                else:
                    # previous zombie carrying over
                    p = prob(A, B, i-1, 0, H[h])
                    dp_zombie[(i+1)%2][h] = add(dp_zombie[(i+1)%2][h], mult(dp_zombie[i%2][h], p))
                    # not carrying over
                    p = sub(1, p)
                    if z:  # new zombie
                        dp_zombie[(i+1)%2][z] = add(dp_zombie[(i+1)%2][z], mult(dp_zombie[i%2][h], p))
                    else:  # now safe 
                        dp_safe[(i+1)%2][0] = add(dp_safe[(i+1)%2][0], mult(dp_zombie[i%2][h], p))
            if dp_safe[i%2][h]:
                if z >= h:  # new zombie's at least as tall
                    # new fence is no taller than the zombie
                    p = prob(A, B, i-1, 0, H[z])
                    dp_zombie[(i+1)%2][z] = add(dp_zombie[(i+1)%2][z], mult(dp_safe[i%2][h], p))
                    # new fence is taller
                    accu[z+1] = add(accu[z+1], dp_safe[i%2][h])  # accumulate
                else:
                    # new fence is not taller
                    p = prob(A, B, i-1, 0, H[h])
                    dp_safe[(i+1)%2][h] = add(dp_safe[(i+1)%2][h], mult(dp_safe[i%2][h], p))
                    # new fence is taller
                    accu[h+1] = add(accu[h+1], dp_safe[i%2][h])  # accumulate
        safe_but_not_taller_than_h_prob = 0
        for h in xrange(1, len(H)):
            safe_but_not_taller_than_h_prob = add(safe_but_not_taller_than_h_prob, accu[h])
            if safe_but_not_taller_than_h_prob:
                p = prob(A, B, i-1, H[h-1]+1, H[h])
                dp_safe[(i+1)%2][h] = add(dp_safe[(i+1)%2][h], mult(safe_but_not_taller_than_h_prob, p))
    return reduce(add, dp_safe[N%2])

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, evening_of_the_living_dead())
