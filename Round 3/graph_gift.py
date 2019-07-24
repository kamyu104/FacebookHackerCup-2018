# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 3 - Graph Gift
# https://www.facebook.com/hackercup/problem/234060297329233/
#
# Time:  O(N^2)
# Space: O(N)
#

def cost_of_cross_pairing_B(lookup, B, ny):  # Time: O(N)
    if lookup[ny] == -1:
        result = 0
        for i in xrange((ny-1)//2):
            result += B[-i-2]*B[-ny+i]
        lookup[ny] = result
    return lookup[ny]

def min_cost_of_connecting_last_B(lookup, prefix_sum_B, B, n):  # Time: O(N)
    if not n:
        return 0
    if n == 1 and len(B) >= 2:
        return B[-1]*B[-2]
    
    result = float("inf")
    for y in xrange(1, n):
        if (n-y-1)%2:  # odd
            continue
        curr = B[-1]*(prefix_sum_B[len(B)-n+y]-prefix_sum_B[len(B)-n])
        curr += cost_of_cross_pairing_B(lookup, B, n-y)
        result = min(result, curr)
    return result

def min_cost_of_last_A_paired_with_different_B(lookup, prefix_sum_B, A, B, x):  # Time: O(N)
    result = 0
    for i in xrange(len(A)-x):
        result += -B[0]*A[i]
    for i in xrange(x):
        result += -B[i+1]*A[-x+i]
    result += min_cost_of_connecting_last_B(lookup, prefix_sum_B, B, len(B)-x-1)
    return result

def graph_gift():
    N = input()
    L = map(int, raw_input().strip().split())

    A = [i for i in L if i > 0]
    B = [-i for i in L if i < 0]
    A.sort(reverse=True)
    B.sort(reverse=True)
    if not B:
        A, B = B, A
    prefix_sum_B = [0]*(len(B)+1)
    for i in xrange(len(B)):
        prefix_sum_B[i+1] = prefix_sum_B[i]+B[i]
    lookup = [-1]*len(B)
    result = float("inf")
    if not A:
        result = min_cost_of_connecting_last_B(lookup, prefix_sum_B, B, len(B))  # Time: O(N)
    else:
        for x in xrange(min(len(A), len(B))):  # Time: O(N^2)
            result = min(result, min_cost_of_last_A_paired_with_different_B(lookup, prefix_sum_B, A, B, x))
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, graph_gift())      
