# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 3 - Ethan Finds the Maximum Subarray Sum
# https://www.facebook.com/hackercup/problem/467235440368329/
#
# Time:  O(M^2 * K)
# Space: O(1)
#

def ethan_finds_the_maximum_subarray_sum():
    M, K = map(int, raw_input().strip().split())
    B = map(int, raw_input().strip().split())

    result = 0
    min_ethan_m = max(max(B), 0)
    left = int(B[0] < 0)  # exclude first negative value if it exists
    right = (2*M-1)-int(B[-1] < 0)  # exclude last negative value if it exists
    for ethan_m in xrange(min_ethan_m, (right-left)*K+1):  # enumerate every possible ethan's answer
        max_m, m = 0, 0
        for i in xrange(left, right):  # greedily insert values
            j, is_given_value = divmod(i+1, 2)
            if is_given_value:  # given value
                max_m += B[j]
                m = m+B[j] if B[j] >= 0 else 0
            else:  # inserted value
                next_value = B[j] if (i != right-1 and B[j] >= 0) else 0
                if m+K+next_value <= ethan_m:  # whether to insert K (no decrease to diff)
                    max_m += K
                    m += K
                elif i != right-1:  # insert -1 to maximize diff
                    max_m -= 1
                    m = 0
        result = max(result, max_m-ethan_m)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ethan_finds_the_maximum_subarray_sum())
