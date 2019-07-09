// Copyright (c) 2019 kamyu. All rights reserved.

/*
 * Facebook Hacker Cup 2018 Round 2 - Jack's Candy Shop
 * https://www.facebook.com/hackercup/problem/638251746380051/
 *
 * Time:  O(N * (logN)^2)
 * Space: O(N)
 *
 */

#include <iostream>
#include <vector>
#include <queue>
#include <tuple>

using std::cin;
using std::cout;
using std::endl;
using std::vector;
using std::priority_queue;
using std::tie;
using std::pair;

uint64_t jacks_candy_shop() {
    int T, N, M, A, B;
    cin >> N >> M >> A >> B;
    vector<vector<int>> adj(N);
    for (int i = 1; i < N; ++i) {
        int p;
        cin >> p;
        adj[p].emplace_back(i);
    }
    vector<int> count(N);
    for (int i = 0; i < M; ++i) {
        ++count[(1LL * A * i + B) % N];
    }
  
    uint64_t result = 0ull;
    vector<priority_queue<int>> max_heaps(N);
    vector<pair<int, vector<int>>> stk = {{0, {0}}};
    while (!stk.empty()) {
        int step; vector<int> args;
        tie(step, args) = stk.back();  stk.pop_back();
        if (step == 0) {
            int i = args[0];
            stk.push_back({2, {i}});
            for (const auto& j : adj[i]) {
                stk.push_back({1, {i, j}});
                stk.push_back({0, {j}});
            }
        } else if (step == 1) {
            int i = args[0], j = args[1];
            if (max_heaps[i].size() < max_heaps[j].size()) {
                swap(max_heaps[i], max_heaps[j]);
            }
            while (!max_heaps[j].empty()) {
                max_heaps[i].emplace(max_heaps[j].top()); max_heaps[j].pop();
            }
        } else {
            int i = args[0];
            max_heaps[i].emplace(i);
            while (count[i] && !max_heaps[i].empty()) {
                --count[i];
                result += max_heaps[i].top(); max_heaps[i].pop();
            }
        }
    }
    return result;
}

int main() {
    int T;
    cin >> T;
    for (int test = 1; test <= T; ++test) {
        cout << "Case #" << test << ": " << jacks_candy_shop() << endl;
    }
    return 0;
}