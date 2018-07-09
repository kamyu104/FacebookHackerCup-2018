# Copyright (c) 2018 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Qualification Round - Interception
# https://www.facebook.com/hackercup/problem/175329729852444/
#
# Time:  O(N)
# Space: O(1)
#

def interception():
    N = input()
    for _ in xrange(N+1):
        _ = input()
    return "1\n0.0" if N % 2 == 1 else "0"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, interception())
