# [FacebookHackerCup-2018](https://www.facebook.com/hackercup/past_rounds/) ![Language](https://img.shields.io/badge/language-Python-orange.svg) [![License](https://img.shields.io/badge/license-CC%203.0-blue.svg)](https://creativecommons.org/licenses/by-nc/3.0/) ![Progress](https://img.shields.io/badge/progress-18%20%2F%2021-ff69b4.svg)


Python solutions of Facebook Hacker Cup 2018. Solution begins with `*` means it will get TLE in the largest data set (total computation amount > `10^8`, which is not friendly for Python to solve in 5 ~ 15 seconds). A `6-minute` timer is set for uploading the result this year.

* [Qualification Round](https://github.com/kamyu104/FacebookHackerCup-2018#qualification-round)
* [Round 1](https://github.com/kamyu104/FacebookHackerCup-2018#round-1)
* [Round 2](https://github.com/kamyu104/FacebookHackerCup-2018#round-2)
* [Round 3](https://github.com/kamyu104/FacebookHackerCup-2018#round-3)
* [Final Round](https://github.com/kamyu104/FacebookHackerCup-2018#final-round)

## Qualification Round
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [Tourist](https://www.facebook.com/hackercup/problem/1632703893518337/)| [Python](./Qualification%20Round/tourist.py)| _O(K)_ | _O(1)_ | Easy | | Math |
|2| [Interception](https://www.facebook.com/hackercup/problem/175329729852444/)| [Python](./Qualification%20Round/interception.py)| _O(1)_ | _O(1)_ | Easy | | Math |
|3| [Ethan Searches for a String](https://www.facebook.com/hackercup/problem/1153996538071503/)| [Python](./Qualification%20Round/ethan-searches-for-a-string.py)| _O(N)_ | _O(1)_ | Easy | | String |

## Round 1
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [Let It Flow](https://www.facebook.com/hackercup/problem/180494849326631/)| [Python](./Round%201/let-it-flow.py)| _O(N)_ | _O(W)_ | Easy | | DP |
|2| [Ethan Traverses a Tree](https://www.facebook.com/hackercup/problem/232395994158286/)| [Python](./Round%201/ethan-traverses-a-tree.py)| _O(N)_ | _O(N)_ | Easy | | Graph |
|3| [Platform Parkour](https://www.facebook.com/hackercup/problem/1892930427431211/)| [Python](./Round%201/platform-parkour.py)| _O(N * (M + logZ))_ | _O(N)_ | Medium | | Intervals |
|4| [Evening of the Living Dead](https://www.facebook.com/hackercup/problem/359971574540051/)| [Python](./Round%201/evening-of-the-living-dead.py)| _O(N * M)_ | _O(N)_ | Hard | | DP, Probability |

## Round 2
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [Ethan Finds the Shortest Path](https://www.facebook.com/hackercup/problem/988017871357549/)| [Python](./Round%202/ethan_finds_the_shortest_path.py)| _O(N)_ | _O(1)_ | Easy | | Graph, Greedy |
|2| [Jack's Candy Shop](https://www.facebook.com/hackercup/problem/638251746380051/)| [Python](./Round%202/jacks_candy_shop.py)| _O(N * (logN)^2)_ | _O(N)_ | Medium | | Greedy, Heap, Stack, Recursion |
|3| [Replay Value](https://www.facebook.com/hackercup/problem/271442536778669/)| [PyPy](./Round%202/replay_value.py)| _O(N^5)_ | _O(N^4)_ | Hard | | DP |
|4| [Fossil Fuels](https://www.facebook.com/hackercup/problem/469838700128124/)| [PyPy](./Round%202/fossil_fuels.py)| _O(NlogN)_ | _O(N)_ | Hard | | DP, Mono Deque, Segment Tree, RMQ |

## Round 3
| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [Jammin'](https://www.facebook.com/hackercup/problem/1851349144951409/)| [Python](./Round%203/jammin.py)| _O(N)_ | _O(1)_ | Easy | | Simulation |
|2| [Ethan Finds the Maximum Subarray Sum](https://www.facebook.com/hackercup/problem/467235440368329/)| [Python](./Round%203/ethan_finds_the_maximum_subarray_sum.py)| _O(M^2 * K)_ | _O(1)_ | Medium | | Greedy |
|3| [Graph Gift](https://www.facebook.com/hackercup/problem/234060297329233/)| [PyPy](./Round%203/graph_gift.py)| _O(N^2)_ | _O(N)_ | Medium | | Greedy |
|4| [Finshakes](https://www.facebook.com/hackercup/problem/206776773482750/)| [Python](./Round%203/finshakes.py)| _O(M^3)_ | _O(M^2)_ | Hard | | DP |

## Final Round
You can relive the magic of the 2018 Hacker Cup World Finals by watching the [Live Stream Recording](https://www.facebook.com/hackercup/videos/1066267066866252/) of the announcement of winners.

| # | Title | Solution | Time | Space | Difficulty | Tag | Note |
|---| ----- | -------- | ---- | ----- | ---------- | --- | ---- |
|1| [Contest Environment](https://www.facebook.com/hackercup/problem/1983047265329089/)| [Python](./Final%20Round/contest_environment.py) | _O(N)_ | _O(1)_ | Easy | | Math |
|2| [Stockholm](https://www.facebook.com/hackercup/problem/2019100985085971/)| [Python](./Final%20Round/stockholm.py) | _O(logA + logB)_ | _O(logA + logB)_ | Easy | | Binary Tree, Bit Manipulation, Greedy |
|3| [Ethan Sums Shortest Distances](https://www.facebook.com/hackercup/problem/278591946122939/)| [Python](./Final%20Round/ethan_sums_shortest_distances.py) [Python](./Final%20Round/ethan_sums_shortest_distances2.py) [Python](./Final%20Round/ethan_sums_shortest_distances3.py) [Python](./Final%20Round/ethan_sums_shortest_distances4.py) | _O(N^3)_ | _O(N^2)_ | Easy | | DP |
|4| [Personal Space](https://www.facebook.com/hackercup/problem/659927157741948/)| | | | Medium | | |
|5| [City Lights](https://www.facebook.com/hackercup/problem/162710881087828/)| | | | Hard | | |
|6| [The Claw](https://www.facebook.com/hackercup/problem/278597692763175/)| | | | Medium | | |
