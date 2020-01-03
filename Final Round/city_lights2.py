# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - City Lights
# https://www.facebook.com/hackercup/problem/162710881087828/
#
# Time:  O(S * (W + S) * W^2)
# Space: O(S * (W + S) * W)
#

from collections import defaultdict
from bisect import bisect_left

def add(a, b):
    return (a+b)%MOD

def compute_accu(i, dp, dp_accu):
    for h in xrange(len(dp[i])):
        for b in xrange(len(dp[i][h])):
            dp_accu[i][h+1][b] = add(dp_accu[i][h][b], dp[i][h][b])
 
def city_lights_helper(i, children, building_heights, window_heights, dp, dp_accu):
    dp[i][0][0] = 1
    for c in children[i]:  # O(S) times
        city_lights_helper(c, children, building_heights, window_heights, dp, dp_accu)
        compute_accu(i, dp, dp_accu), compute_accu(c, dp, dp_accu)
        tmp = [[0 for _ in xrange(len(dp[i][h]))] for h in xrange(len(dp[i]))]
        for h in xrange(len(dp[i])):  # O(W+S) times
            for b in xrange(len(dp[i][h])):  # O(W) times
                for b2 in xrange(len(dp[i][h])-b):  # O(W) times
                    tmp[h][b+b2] = add(tmp[h][b+b2], dp[i][h][b]*dp_accu[c][h+1][b2] + dp_accu[i][h][b]*dp[c][h][b2])
        dp[i][:] = tmp

    window_heights[i].sort()
    tmp = [[0 for _ in xrange(len(dp[i][h]))] for h in xrange(len(dp[i]))]
    power = 1
    for j in xrange(len(window_heights[i])+1):
        h2 = window_heights[i][j-1] if j-1 >= 0 else 0
        for h in xrange(len(dp[i])):
            for b in xrange(len(dp[i][h])):
                tmp[max(h, h2)][b] = add(tmp[max(h, h2)][b], power*dp[i][h][b])
        if j-1 >= 0:
            power *= 2
    dp[i][:] = tmp

    for h in xrange(building_heights[i], len(dp[i])):
        for b in xrange(len(dp[i][h])-1):
            dp[i][0][b+1] = add(dp[i][0][b+1], dp[i][h][b])
            dp[i][h][b] = 0

def city_lights():
    W, S = map(int, raw_input().strip().split())
    W_P, S_P = [None]*W, [None]*S
    y_set = set([0])
    for i in xrange(W):
        W_P[i]= map(int, raw_input().strip().split())
        y_set.add(W_P[i][Y])
    for i in xrange(S):
        S_P[i]= map(int, raw_input().strip().split())
        y_set.add(S_P[i][Y])
    max_x = max(map(max, [W_P, S_P]))[X]
    
    order = {}
    for i, y in enumerate(sorted(y_set)):  # Time: O((W+S)log(W+S))
        order[y] = i
    for i in xrange(W):
        W_P[i][Y] = order[W_P[i][Y]]
    for i in xrange(S):
        S_P[i][Y] = order[S_P[i][Y]]

    S_P.sort(key=lambda x: x[Y])  # Time: O(SlogS)
    children = defaultdict(list)
    ordered_set, building_heights, lookup = [((0, max_x+1), 0)], [1], {}
    for x, y in S_P:  # Time: O(S^2)
        (a, b), c = ordered_set[bisect_left(ordered_set, ((x, max_x+2), 0))-1]
        if not a <= x <= b:
            continue
        if a < x:
            children[c].append(len(building_heights))
            ordered_set.insert(bisect_left(ordered_set, ((a, x-1), len(building_heights))), ((a, x-1), len(building_heights)))
            building_heights.append(y)
        if b > x:
            children[c].append(len(building_heights))
            ordered_set.insert(bisect_left(ordered_set, ((x+1, b), len(building_heights))), ((x+1, b), len(building_heights)))
            building_heights.append(y)
        ordered_set.remove(((a, b), c))
        lookup[x] = c

    window_heights = defaultdict(list)
    for x, y in W_P:  # Time: O(WlogS)
        c = lookup[x] if x in lookup else ordered_set[bisect_left(ordered_set, ((x, max_x+2), 0))-1][1]
        window_heights[c].append(y)

    dp = [[[0 for _ in xrange(len(W_P)+1)] for _ in xrange(len(y_set))] for _ in xrange(len(building_heights))]
    dp_accu = [[[0 for _ in xrange(len(W_P)+1)] for _ in xrange(len(y_set)+1)] for _ in xrange(len(building_heights))]
    city_lights_helper(0, children, building_heights, window_heights, dp, dp_accu)  # Time: O(S*(W+S)*W^2)
    result = 0
    for i in xrange(1, len(dp[0][0])):
        result = add(result, i*dp[0][0][i])
    return result

MOD = 10**9+7
X, Y = range(2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, city_lights())
