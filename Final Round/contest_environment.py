# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Final Round - Contest Environment
# https://www.facebook.com/hackercup/problem/1983047265329089/
#
# Time:  O(N)
# Space: O(1)
#

def contest_environment():
    A, B = raw_input().strip(), raw_input().strip()
    if any(x == '#' for x in B):
        return "Impossible"
    unoccupied_count = sum(int(x == '.') for x in A) + sum(int(x == '.') for x in B)
    max_blocked_count, blocked_count = 0, 0
    for x in A:
        if x == '#':
            blocked_count += 1
        else:
            max_blocked_count = max(max_blocked_count, blocked_count)
            blocked_count = 0
    return "Possible" if (unoccupied_count >= max_blocked_count + 3) else "Impossible"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, contest_environment())
