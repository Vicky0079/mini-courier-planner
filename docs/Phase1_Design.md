# Phase 1 - Courier Problem Design and Planning

## 1. Problem Statement
Given a set of parcels with weights, priorities, deadlines, and delivery
destinations, and a weighted undirected graph of delivery points, produce:
1. A prioritized order of parcels.
2. An optimal subset of parcels that fits one delivery trip.
3. A delivery route starting and ending at the depot.

## 2. Parcel Attributes
| Attribute | Type | Meaning |
|---|---|---|
| pid | string | Unique parcel ID |
| weight | int | Parcel weight (knapsack cost) |
| priority | int | Business value (knapsack value) |
| deadline | int | Hours until delivery deadline |
| destination | string | Graph node for delivery |

## 3. Graph Format
- Stored as JSON: `{ "nodes": [...], "edges": [[u, v, w], ...] }`
- Loaded into an adjacency list: `node -> [(neighbor, weight), ...]`
- Undirected, non-negative weights (required by Dijkstra).

## 4. Algorithm Selection
| Step | Algorithm | Time | Why |
|---|---|---|---|
| Prioritize parcels | Timsort | O(n log n) | Best general-purpose stable sort |
| Select parcels | 0/1 Knapsack DP | O(n x C) | Guarantees optimal value for integer weights |
| Shortest paths | Dijkstra (heapq) | O((V+E) log V) | Non-negative weights, faster than Bellman-Ford |
| Delivery route | Nearest-neighbor TSP | O(k^2) approx | TSP is NP-hard; NN gives fast feasible tours |

## 5. Integration Flow
sort(parcels) -> knapsack(sorted) -> delivery_nodes -> dijkstra -> NN-TSP -> route