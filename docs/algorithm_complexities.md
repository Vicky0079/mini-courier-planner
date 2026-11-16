# Algorithm Complexities

| Component | Algorithm | Time | Space |
|---|---|---|---|
| Parcel prioritization | Timsort (Python sorted) | O(n log n) | O(n) |
| Packing optimization | 0/1 Knapsack DP | O(n * capacity) | O(n * capacity) |
| Shortest path | Dijkstra (binary heap) | O((V+E) log V) | O(V + E) |
| Route planning | Nearest-neighbor TSP | O(k^2) after APSP | O(k^2) |
| APSP (metric closure) | Dijkstra from each node | O(V * (V+E) log V) | O(V^2) |

Where:
- n = number of parcels
- V = number of graph nodes
- E = number of edges
- k = number of delivery destinations visited
- capacity = knapsack weight limit