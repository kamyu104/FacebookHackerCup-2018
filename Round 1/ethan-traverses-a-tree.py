# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 1 - Ethan Traverses a Tree
# https://www.facebook.com/hackercup/problem/232395994158286/
#
# Time:  O(N)
# Space: O(N)
#

def preorder_traversal(tree, i, preorder):
    preorder.append(i)
    if tree[i][0] != 0:
        preorder_traversal(tree, tree[i][0], preorder)
    if tree[i][1] != 0:
        preorder_traversal(tree, tree[i][1], preorder)

def postorder_traversal(tree, i, postorder):
    if tree[i][0] != 0:
        postorder_traversal(tree, tree[i][0], postorder)
    if tree[i][1] != 0:
        postorder_traversal(tree, tree[i][1], postorder)
    postorder.append(i)

def invert_idx(array):
    invert_idx_array = [0] * len(array)
    for i, x in enumerate(array):
        invert_idx_array[x] = i
    return invert_idx_array

def ethan_traverses_a_tree():
    N, K = map(int, raw_input().strip().split())
    tree = [None]*N
    for i in xrange( N):
        tree[i] = map(int, raw_input().strip().split())
        tree[i][0] -= 1 if tree[i][0] != 0 else 0
        tree[i][1] -= 1 if tree[i][1] != 0 else 0

    orders = [[] for _ in xrange(2)]
    preorder_traversal(tree, 0, orders[0])
    postorder_traversal(tree, 0, orders[1])
    idxs = map(invert_idx, orders)

    result = [0]*N
    unlabeled_nodes = set(range(N))
    possible = False
    while unlabeled_nodes:
        for label in xrange(1, K+1):
            if not unlabeled_nodes:
                if possible:
                    break
                return "Impossible"
            node = unlabeled_nodes.pop()
            result[node] = label
            nei = orders[1][idxs[0][node]]
            while result[nei] == 0:
                unlabeled_nodes.discard(nei)
                result[nei] = label
                nei = orders[1][idxs[0][nei]]
        possible = True
    return " ".join(map(str, result))

import sys
sys.setrecursionlimit(2000)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_traverses_a_tree())
