# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - City Lights
# https://www.facebook.com/hackercup/problem/162710881087828/
#
# Time:  O(S * W^3), there is no built-in rbtree in python, so we can use skip list alternatively,
#                    which implementation is much simpler than rbtree
#                    and has the same complexity on average
# Space: O(S * W^2)
#

# based on official solution:
# dp[i][h][b] = # of combinations in i's subtree requiring b buildings, with height h still required
# dp_accu[i][h][b] = sum of dp[i][0..(h-1)][b]

from collections import defaultdict
from random import randint, seed

# Template:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/design-skiplist.py
class SkipNode(object):
    def __init__(self, level=0, val=None):
        self.val = val
        self.nexts = [None]*level
        self.prevs = [None]*level

class SkipList(object):
    P_NUMERATOR, P_DENOMINATOR = 1, 2  # P = 1/4 in redis implementation
    MAX_LEVEL = 32  # enough for 2^32 elements

    def __init__(self, end=float("inf"), can_duplicated=False):
        seed(0)
        self.__head = SkipNode()
        self.__len = 0
        self.__can_duplicated = can_duplicated
        self.add(end)
    
    def lower_bound(self, target):
        return self.__lower_bound(target, self.__find_prev_nodes(target))

    def find(self, target):
        return self.__find(target, self.__find_prev_nodes(target))
        
    def add(self, val):
        if not self.__can_duplicated and self.find(val):
            return False
        node = SkipNode(self.__random_level(), val)
        if len(self.__head.nexts) < len(node.nexts): 
            self.__head.nexts.extend([None]*(len(node.nexts)-len(self.__head.nexts)))
        prevs = self.__find_prev_nodes(val)
        for i in xrange(len(node.nexts)):
            node.nexts[i] = prevs[i].nexts[i]
            if prevs[i].nexts[i]:
                prevs[i].nexts[i].prevs[i] = node
            prevs[i].nexts[i] = node
            node.prevs[i] = prevs[i]
        self.__len += 1
        return True

    def remove(self, val):
        prevs = self.__find_prev_nodes(val)
        curr = self.__find(val, prevs)
        if not curr:
            return False
        self.__len -= 1   
        for i in reversed(xrange(len(curr.nexts))):
            prevs[i].nexts[i] = curr.nexts[i]
            if curr.nexts[i]:
                curr.nexts[i].prevs[i] = prevs[i]
            if not self.__head.nexts[i]:
                self.__head.nexts.pop()
        return True
    
    def __lower_bound(self, val, prevs):
        if prevs:
            candidate = prevs[0].nexts[0]
            if candidate:
                return candidate
        return None

    def __find(self, val, prevs):
        candidate = self.__lower_bound(val, prevs)
        if candidate and candidate.val == val:
            return candidate
        return None

    def __find_prev_nodes(self, val):
        prevs = [None]*len(self.__head.nexts)
        curr = self.__head
        for i in reversed(xrange(len(self.__head.nexts))):
            while curr.nexts[i] and curr.nexts[i].val < val:
                curr = curr.nexts[i]
            prevs[i] = curr
        return prevs

    def __random_level(self):
        level = 1
        while randint(1, SkipList.P_DENOMINATOR) <= SkipList.P_NUMERATOR and \
              level < SkipList.MAX_LEVEL:
            level += 1
        return level

    def __len__(self):
        return self.__len-1  # excluding end node
    
    def __str__(self):
        result = []
        for i in reversed(xrange(len(self.__head.nexts))):
            result.append([])
            curr = self.__head.nexts[i]
            while curr:
                result[-1].append(str(curr.val))
                curr = curr.nexts[i]
        return "\n".join(map(lambda x: "->".join(x), result))

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
            for b in xrange(len(dp[i][h])):  # O(W) times
                for b2 in xrange(len(dp[i][h])-b):  # O(W) times
                    # new_dp[i][h][b+b2] = dp[i][h][b]*dp[c][h][b2] + dp[i][h][b]*dp[c][0..(h-1)][b2] + dp[i][0..(h-1)][b]*dp[c][h][b2]
                    tmp[h][b+b2] = add(tmp[h][b+b2], dp[i][h][b]*dp_accu[c][h+1][b2] + dp_accu[i][h][b]*dp[c][h][b2])
        dp[i][:] = tmp

    window_heights[i].sort()
    tmp = [[0 for _ in xrange(len(dp[i][h]))] for h in xrange(len(dp[i]))]
    power = 1
    for j in xrange(len(window_heights[i])+1):  # O(W) times
        h2 = window_heights[i][j-1] if j-1 >= 0 else 0
        for h in xrange(len(dp[i])):  # O(W) times
            for b in xrange(len(dp[i][h])):  # O(W) times
                tmp[max(h, h2)][b] = add(tmp[max(h, h2)][b], power*dp[i][h][b])  # count # of combinations
        if j-1 >= 0:
            power = multiply(power, 2)
    dp[i][:] = tmp

    for h in xrange(1, len(dp[i])):  # O(W) times
        if idx_to_height[h] < building_height[i]:
            continue
        for b in xrange(len(dp[i][h])-1):  # O(W) times
            dp[i][0][b+1] = add(dp[i][0][b+1], dp[i][h][b])  # make this node as a new building with height h
            dp[i][h][b] = 0  # no need to keep tracking count on any not-yet-satisfied path

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
    
    order = {}
    for i, y in enumerate(sorted(y_set)):  # Time: O((W+S)log(W+S)), coordinate compression of y
        order[y] = i
    for i in xrange(W):
        W_P[i][Y] = order[W_P[i][Y]]
    for i in xrange(S):
        S_P[i][Y] = order[S_P[i][Y]]
    
    w_y_set = set([0])
    for x, y in W_P:
        w_y_set.add(y)
    idx_to_height, height_to_idx = [], {}
    for i, y in enumerate(sorted(w_y_set)):  # Time: O(WlogW), coordinate compression of y of W
        idx_to_height.append(y)
        height_to_idx[y] = i

    S_P.sort(key=lambda x: x[Y])  # Time: O(SlogS)
    children = defaultdict(list)
    ordered_set, building_height, lookup = SkipList(((float("inf"), float("inf")), float("inf"))), [1], {}
    ordered_set.add(((float("-inf"), float("inf")), 0))
    for x, y in S_P:  # Time: O(SlogS), split intervals by x of star in non-decreasing order of y to build up binary tree
        (a, b), c = ordered_set.lower_bound(((x, float("inf")), float("inf"))).prevs[0].val
        if not a <= x <= b:
            continue
        if a < x:
            children[c].append(len(building_height))
            ordered_set.add(((a, x-1), len(building_height)))
            building_height.append(y)
        if b > x:
            children[c].append(len(building_height))
            ordered_set.add(((x+1, b), len(building_height)))
            building_height.append(y)
        ordered_set.remove(((a, b), c))
        lookup[x] = c

    window_heights = defaultdict(list)
    for x, y in W_P:  # Time: O(WlogS), group windows by tree nodes
        c = lookup[x] if x in lookup else ordered_set.lower_bound(((x, float("inf")), float("inf"))).prevs[0].val[1]
        window_heights[c].append(height_to_idx[y])

    dp = [[[0 for _ in xrange(len(W_P)+1)] for _ in xrange(len(w_y_set))] for _ in xrange(len(building_height))]
    dp_accu = [[[0 for _ in xrange(len(W_P)+1)] for _ in xrange(len(w_y_set)+1)] for _ in xrange(len(building_height))]
    city_lights_helper(0, children, building_height, window_heights, idx_to_height, dp, dp_accu)  # Time: O(S*W^3)
    result = 0
    for i in xrange(1, len(dp[0][0])):  # Time: O(W), compute expected number
        result = add(result, i*dp[0][0][i])
    return result

MOD = 10**9+7
X, Y = range(2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, city_lights())
