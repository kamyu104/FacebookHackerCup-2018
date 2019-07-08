# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 2 - Ethan Path
# https://www.facebook.com/hackercup/problem/988017871357549/
#
# Time:  O(N)
# Space: O(1)
#

def ethan_path():
    N, K = map(int, raw_input().strip().split())

    result = ["0", "1"]
    diff = K
    result.append("%d %d %d" % (1, N, K))
    K -= 1
    if not (N-1 >= 2 and K >= 2):
        return "\n".join(result)
    for i in xrange(2, N):
        diff -= K
        result.append("%d %d %d" % (i-1, i, K))
        K -= 1
        if K == 1 or i == N-1:
            diff -= K
            result.append("%d %d %d" % (i, N, K))
            break
    result[0], result[1] = str(abs(diff)), str(len(result)-2)
    return "\n".join(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_path())

