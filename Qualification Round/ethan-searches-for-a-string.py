# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Qualification Round - Ethan Searches for a String
# https://www.facebook.com/hackercup/problem/1153996538071503/
#
# Time:  O(N^2)
# Space: O(1)
#

def ethan_searches_for_a_string():
    A = raw_input().strip()
    for i in xrange(1, len(A)):
        if A[i] == A[0]:
            for j in xrange(len(A)):
                if A[j] != A[j%i]:
                    return A[:i]+A
    return "Impossible"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_searches_for_a_string())
