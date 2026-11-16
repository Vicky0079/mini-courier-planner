# Viva Questions and Answers

**Q1. Why Timsort and not Quicksort?**
Timsort is O(n log n) in the worst case, stable, and exploits already-sorted
runs (common when parcels arrive in deadline order). Python built-in sorted()
uses Timsort. Quicksort is O(n^2) worst case.

**Q2. Why 0/1 Knapsack and not fractional?**
Each parcel is indivisible; you cannot split a parcel across two trips.
Fractional knapsack (greedy by value/weight) is for divisible goods.

**Q3. Why is Knapsack DP pseudo-polynomial?**
Runtime O(n * capacity) depends on the numeric value of capacity, not just
the bit-length of the input. Large capacity makes it slow.

**Q4. Why Dijkstra and not Bellman-Ford?**
All edge weights are non-negative, so Dijkstra is faster:
O((V+E) log V) vs O(V * E) for Bellman-Ford.

**Q5. When would Dijkstra fail?**
With negative edge weights, because it never revisits a settled node.

**Q6. Why nearest-neighbor TSP and not exact TSP?**
Exact TSP is O(n^2 * 2^n) - infeasible for realistic n. NN gives a
feasible route in O(k^2) (after APSP). It is an approximation, so it is
not guaranteed optimal, but it is fast and good enough for a courier
prototype.

**Q7. What is the time complexity of your full pipeline?**
- sort: O(n log n)
- knapsack: O(n * capacity)
- dijkstra per node + APSP: O(k * (V+E) log V)
- NN-TSP: O(k^2)
- Overall dominated by max of these.

**Q8. How would you improve routing?**
Use 2-opt or Or-opt local search to improve the NN tour; or use Christofides
(1.5-approximation) or an exact DP for small k (< 20).

**Q9. How would you improve knapsack for many parcels?**
Use branch-and-bound or meet-in-the-middle; or reduce capacity by rounding
weights (scaled FPTAS).

**Q10. How does capacity affect selection?**
Lower capacity -> fewer parcels -> lower total priority but tighter packing.
Higher capacity -> more parcels -> higher total priority but longer route.

**Q11. Why save DP table as evidence?**
It shows the optimal subproblem values, letting the evaluator verify the
backtracking selected the optimal subset.

**Q12. What is the difference between route length and shortest-path distance?**
Shortest-path distance is pairwise (Dijkstra). Route length sums the
shortest-path distances along the chosen visiting order, including return
to depot.