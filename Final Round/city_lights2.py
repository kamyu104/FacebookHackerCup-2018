# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - City Lights
# https://www.facebook.com/hackercup/problem/162710881087828/
#
# Time:  O(S^2 * W^2)
# Space: O(S * W * min(S, W))
#

# based on official solution:
# dp[i][h][b] = # of combinations in i's subtree requiring b buildings, with height h still required
# dp_accu[i][h][b] = sum of dp[i][0..(h-1)][b]

from collections import defaultdict
from bisect import bisect_left

def add(a, b):
    return (a+b)%MOD

def multiply(a, b):
    return (a*b)%MOD

def compute_accu(i, dp, dp_accu):
    for h in xrange(len(dp[i])):
        for b in xrange(len(dp[i][h])):
            dp_accu[i][h+1][b] = add(dp_accu[i][h][b], dp[i][h][b])
 
def city_lights_helper(i, children, building_height, window_heights, idx_to_height, dp, dp_accu):
    dp[i][0][0] = 1
    for c in children[i]:  # O(2) times
        city_lights_helper(c, children, building_height, window_heights, idx_to_height, dp, dp_accu)
        compute_accu(i, dp, dp_accu), compute_accu(c, dp, dp_accu)
        tmp = [[0 for _ in xrange(len(dp[i][h]))] for h in xrange(len(dp[i]))]
        for h in xrange(len(dp[i])):  # O(W) times
            for b in xrange(len(dp[i][h])):  # O(min(S, W)) times
                for b2 in xrange(len(dp[i][h])-b):  # O(min(S, W)) times
                    # new_dp[i][h][b+b2] = dp[i][h][b]*dp[c][h][b2] + dp[i][h][b]*dp[c][0..(h-1)][b2] + dp[i][0..(h-1)][b]*dp[c][h][b2]
                    tmp[h][b+b2] = add(tmp[h][b+b2], dp[i][h][b]*dp_accu[c][h+1][b2] + dp_accu[i][h][b]*dp[c][h][b2])
        dp[i][:] = tmp

    window_heights[i].sort()
    tmp = [[0 for _ in xrange(len(dp[i][h]))] for h in xrange(len(dp[i]))]
    power = 1
    for j in xrange(len(window_heights[i])+1):  # O(W) times
        h2 = window_heights[i][j-1] if j-1 >= 0 else 0
        for h in xrange(len(dp[i])):  # O(W) times
            for b in xrange(len(dp[i][h])):  # O(min(S, W)) times
                tmp[max(h, h2)][b] = add(tmp[max(h, h2)][b], power*dp[i][h][b])  # count # of combinations
        if j-1 >= 0:
            power = multiply(power, 2)
    dp[i][:] = tmp

    for h in xrange(1, len(dp[i])):  # O(W) times
        if idx_to_height[h] < building_height[i]:
            continue
        for b in xrange(len(dp[i][h])-1):  # O(min(S, W)) times
            dp[i][0][b+1] = add(dp[i][0][b+1], dp[i][h][b])  # make this node as a new building with height h
            dp[i][h][b] = 0  # no need to keep tracking count on any not-yet-satisfied path

def city_lights():
    W, S = map(int, raw_input().strip().split())
    W_P, S_P = [None]*W, [None]*S
    w_y_set = set([0])
    for i in xrange(W):
        W_P[i]= map(int, raw_input().strip().split())
        w_y_set.add(W_P[i][Y])
    for i in xrange(S):
        S_P[i]= map(int, raw_input().strip().split())

    idx_to_height, height_to_idx = [], {}
    for i, y in enumerate(sorted(w_y_set)):  # Time: O(WlogW), coordinate compression of y of W
        idx_to_height.append(y)
        height_to_idx[y] = i

    S_P.sort(key=lambda x: x[Y])  # Time: O(SlogS)
    children = defaultdict(list)
    ordered_set, building_height, lookup = [((float("-inf"), float("inf")), 0)], [1], {}
    for x, y in S_P:  # Time: O(S^2), split intervals by x of star in non-decreasing order of y to build up binary tree
        (a, b), c = ordered_set[bisect_left(ordered_set, ((x, float("inf")), float("inf")))-1]
        if not a <= x <= b:
            continue
        if a < x:
            children[c].append(len(building_height))
            ordered_set.insert(bisect_left(ordered_set, ((a, x-1), len(building_height))), ((a, x-1), len(building_height)))
            building_height.append(y)
        if b > x:
            children[c].append(len(building_height))
            ordered_set.insert(bisect_left(ordered_set, ((x+1, b), len(building_height))), ((x+1, b), len(building_height)))
            building_height.append(y)
        ordered_set.remove(((a, b), c))
        lookup[x] = c

    window_heights = defaultdict(list)
    for x, y in W_P:  # Time: O(WlogS), group windows by tree nodes
        c = lookup[x] if x in lookup else ordered_set[bisect_left(ordered_set, ((x, float("inf")), float("inf")))-1][1]
        window_heights[c].append(height_to_idx[y])

    dp = [[[0 for _ in xrange(min(len(building_height), len(W_P))+1)] for _ in xrange(len(w_y_set))] for _ in xrange(len(building_height))]
    dp_accu = [[[0 for _ in xrange(min(len(building_height), len(W_P))+1)] for _ in xrange(len(w_y_set)+1)] for _ in xrange(len(building_height))]
    city_lights_helper(0, children, building_height, window_heights, idx_to_height, dp, dp_accu)  # Time: O(S^2*W^2)
    result = 0
    for i in xrange(1, len(dp[0][0])):  # Time: O(min(S, W)), compute expected number
        result = add(result, i*dp[0][0][i])
    return result

MOD = 10**9+7
X, Y = range(2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, city_lights())
