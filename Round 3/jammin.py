# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2018 Round 3 - Jammin'
# https://www.facebook.com/hackercup/problem/1851349144951409/
#
# Time:  O(N)
# Space: O(1)
#

def jammin():
    C = list(raw_input())
    C += [' ', ' ']

    result, curr, past, can_pick_past = 0, 0, 0, False
    i = 0
    while i < len(C):
        if C[i] == '*':
            curr += 1
            if curr >= 2 or can_pick_past:
                curr += past
                past, can_pick_past = 0, False
            result = max(result, curr)
        elif C[i] == '#' and C[i+1] != '#':  # 1 barrier
            if curr < 2:
                if C[i+1] == '*':
                    can_pick_past = False
                elif curr:  # place one, and pick back later if find next jammer
                    curr -= 1
                    past += 1
                    can_pick_past = True
                else:
                    break  # stop
        elif C[i] == '#' and C[i+1] == '#' and C[i+2] != '#':  # 2 barriers
            if curr and C[i+2] == '*':  # swap
                i += 2
            else:
                break  # stop
        elif C[i] == '#' and C[i+1] == '#' and C[i+2] == '#':  # 3 barriers
            break  # stop
        i += 1
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, jammin())
