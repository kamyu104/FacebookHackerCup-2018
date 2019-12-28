# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - Personal Space
# https://www.facebook.com/hackercup/problem/659927157741948/
#
# Time:  O(NlogN), there is no built-in rbtree in python, so we can use skip list alternatively,
#                  which implementation is much simpler than rbtree
#                  and has the same complexity on average
# Space: O(N)
#

from random import randint, seed

# Template:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/design-skiplist.py
class SkipNode(object):
    def __init__(self, level=0, val=None):
        self.val = val
        self.nexts = [None]*level
        self.prevs = [None]*level

class Skiplist(object):
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
        while randint(1, Skiplist.P_DENOMINATOR) <= Skiplist.P_NUMERATOR and \
              level < Skiplist.MAX_LEVEL:
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

def add_rect(rects, x1, y1, x2, y2):
    if x2 < 0 or y1 > MAX_X_Y:
        return
    i = len(rects)+1
    rects.append(((y1, 1), (x1, i)))
    rects.append(((y2, 0), (x2, i)))
 
def add_rects(x_ordered_set, rects, x):
    it = x_ordered_set.lower_bound(x)
    for i in xrange(3):
        it = it.prevs[0]
    X = []
    for i in xrange(7):
        X.append(it.val)
        it = it.nexts[0]
    for i in xrange(4):
        add_rect(rects, X[i],X[i+1],X[i+2],X[i+3])
 
def query(x_max_dp_ordered_set, x):
    return x_max_dp_ordered_set.lower_bound((x+1, 0)).prevs[0].val[1]
 
def update(x_max_dp_ordered_set, x, v):
    it = x_max_dp_ordered_set.lower_bound((x+1,0)).prevs[0]
    if v <= it.val[1]:
        return
    if it.val[0] < x:
        it = it.nexts[0]
    while it and v >= it.val[1]:
        curr = it
        it = it.nexts[0]
        x_max_dp_ordered_set.remove(curr.val)
    x_max_dp_ordered_set.add((x, v))

def personal_space():
    N = input()
    intervals = []
    for i in xrange(N):
        X, A, B = map(int, raw_input().strip().split())
        intervals.append((((A, X), 1)))
        intervals.append((((B+1, X), -1)))
    # bottom-up line sweep to generate all possible fish placement "rectangles"
    intervals.sort()
    x_ordered_set = Skiplist()
    for i in xrange(4):
        x_ordered_set.add(-1-i)
        x_ordered_set.add(MAX_X_Y+1+i)
    rects = []
    i = 0
    while i < len(intervals):
        j = i
        while j+1 < len(intervals) and intervals[j+1][0][0] == intervals[i][0][0]:
            j += 1
        for k in xrange(i, j+1):
            if intervals[k][1] > 0:
                x_ordered_set.add(intervals[k][0][1])
            else:
                x_ordered_set.remove(intervals[k][0][1])
        for k in xrange(i, j+1):
            add_rects(x_ordered_set, rects, intervals[k][0][1])
        i = j
        i += 1
    # bottom-up line sweep DP on rectangles
    rects.sort()
    x_max_dp_ordered_set = Skiplist((float("inf"), float("inf")))
    x_max_dp_ordered_set.add((float("-inf"), 0))
    result = 0
    dp = [0]*len(rects)
    for i in xrange(len(rects)):
        x, j = rects[i][1][0], rects[i][1][1]
        if rects[i][0][1]:
            dp[j] = query(x_max_dp_ordered_set, x)+1
            result = max(result, dp[j])
        else:
            update(x_max_dp_ordered_set, x, dp[j])
    return result

MAX_X_Y = 10**9
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, personal_space())
