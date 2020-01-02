# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - City Lights
# https://www.facebook.com/hackercup/problem/162710881087828/
#
# Time:  O(S * (W + S) * W^2), there is no built-in rbtree in python, so we can use skip list alternatively,
#                              which implementation is much simpler than rbtree
#                              and has the same complexity on average
# Space: O(S * (W + S) * W)
#

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

def compute_accu(i, dp, dp_accu):
    for h in xrange(len(dp[i])):
        for b in xrange(len(dp[i][h])):
            dp_accu[i][h+1][b] = add(dp_accu[i][h][b], dp[i][h][b])
 
def city_lights_helper(i, H, children, windows, dp, dp_accu):
    dp[i][0][0] = 1
    for c in children[i]:  # O(S) times
        city_lights_helper(c, H, children, windows, dp, dp_accu)
        compute_accu(i, dp, dp_accu), compute_accu(c, dp, dp_accu)
        tmp = [[0 for _ in xrange(len(dp[i][h]))] for h in xrange(len(dp[i]))]
        for h in xrange(len(dp[i])):  # O(W+S) times
            for b in xrange(len(dp[i][h])):  # O(W) times
                for b2 in xrange(len(dp[i][h])-b):  # O(W) times
                    tmp[h][b+b2] = add(tmp[h][b+b2], dp[i][h][b]*dp_accu[c][h+1][b2] + dp_accu[i][h][b]*dp[c][h][b2])
        dp[i][:] = tmp

    windows[i].sort(reverse=True)
    tmp = [[0 for _ in xrange(len(dp[i][h]))] for h in xrange(len(dp[i]))]
    power = 1
    for j in reversed(xrange(len(windows[i])+1)):
        h2 = windows[i][j] if j < len(windows[i]) else 0
        for h in xrange(len(dp[i])):
            for b in xrange(len(dp[i][h])):
                tmp[max(h, h2)][b] = add(tmp[max(h, h2)][b], power*dp[i][h][b])
        if j < len(windows[i]):
            power *= 2
    dp[i][:] = tmp

    for h in xrange(H[i], len(dp[i])):
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
    
    order = {}
    for i, y in enumerate(sorted(y_set)):  # Time: O((W+S)log(W+S))
        order[y] = i
    for i in xrange(W):
        W_P[i][Y] = order[W_P[i][Y]]
    for i in xrange(S):
        S_P[i][Y] = order[S_P[i][Y]]

    S_P.sort(key=lambda x: x[Y])  # Time: O(SlogS)
    children = defaultdict(list)
    ordered_set, H, lookup = SkipList(((float("inf"), float("inf")), float("inf"))), [1], {}
    ordered_set.add(((0, MAX_X+1), 0))
    for x, y in S_P:  # Time: O(SlogS)
        (a, b), c = ordered_set.lower_bound(((x, MAX_X+2), 0)).prevs[0].val
        if not a <= x <= b:
            continue
        if a < x:
            children[c].append(len(H))
            ordered_set.add(((a, x-1), len(H)))
            H.append(y)
        if b > x:
            children[c].append(len(H))
            ordered_set.add(((x+1, b), len(H)))
            H.append(y)
        ordered_set.remove(((a, b), c))
        lookup[x] = c

    windows = defaultdict(list)
    for x, y in W_P:  # Time: O(WlogS)
        c = lookup[x] if x in lookup else ordered_set.lower_bound(((x, MAX_X+2), 0)).prevs[0].val[1]
        windows[c].append(y)

    dp = [[[0 for _ in xrange(len(W_P)+1)] for _ in xrange(len(y_set))] for _ in xrange(len(H))]
    dp_accu = [[[0 for _ in xrange(len(W_P)+1)] for _ in xrange(len(y_set)+1)] for _ in xrange(len(H))]
    city_lights_helper(0, H, children, windows, dp, dp_accu)  # Time: O(S*(W+S)*W^2)
    result = 0
    for i in xrange(1, len(dp[0][0])):
        result = add(result, i*dp[0][0][i])
    return result

MOD = 10**9+7
MAX_X = 10**9
X, Y = range(2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, city_lights())
