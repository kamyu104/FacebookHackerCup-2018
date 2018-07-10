# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Qualification Round - Ethan Searches for a String
# https://www.facebook.com/hackercup/problem/1153996538071503/
#
# Time:  O(N)
# Space: O(1)
#

def ethan_searches_for_a_string():
    A = raw_input().strip()
    i = A.find(A[0], 1)
    if i != -1:
        l = min(i, len(A)-i)
        if A[i:i+l] != A[:l]:
            return A[:i]+A
    return "Impossible"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_searches_for_a_string())
