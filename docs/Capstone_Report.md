# Mini-Courier Planner — Capstone Report

**Course:** Design & Analysis of Algorithms (ETCCDA302)  
**Programme:** B.Tech CSE & Specializations  
**Faculty:** Dr. Shweta Agarwal

---

## Phase 1 — Courier Problem Design and Planning

### Problem
Given parcels with (weight, priority, deadline, destination) and an undirected weighted graph, produce a prioritized parcel order, an optimal single-trip parcel subset, and a closed delivery route from the depot.

### Parcel attributes
| Attribute | Type | Role |
|---|---|---|
| pid | string | Unique ID |
| weight | int | Knapsack cost |
| priority | int | Knapsack value |
| deadline | int | Sort key (ascending) |
| destination | string | Graph node |

### Graph format
JSON: { "nodes": [...], "edges": [[u,v,w],...] }, loaded as adjacency list. Undirected, non-negative weights.

### Algorithm selection
| Step | Algorithm | Complexity | Rationale |
|---|---|---|---|
| Prioritize | Timsort | O(n log n) | Stable, best general sort |
| Pack | 0/1 Knapsack DP | O(n*C) | Optimal for indivisible parcels |
| Shortest path | Dijkstra (heapq) | O((V+E) log V) | Non-negative weights |
| Route | Nearest-neighbor TSP | O(k^2) approx | TSP is NP-hard |

### Integration flow
sort -> knapsack -> dijkstra(APSP) -> nearest-neighbor TSP -> route

---

## Phase 2 — Package Prioritization and Box Filling

### Sorting
Key: (deadline, -priority). Timsort O(n log n), stable.
Input: P1(d5,p5,w3) P2(d3,p4,w4) P3(d8,p3,w2) P4(d2,p5,w5) P5(d6,p2,w1)  
Sorted: P4 -> P2 -> P1 -> P5 -> P3

### Knapsack DP
Capacity = 8.  
Selected: P2(4w,4p) + P1(3w,5p) + P5(1w,2p) = 8w, 11p  
Optimal priority value = 11 (saved in outputs/dp_table.csv)

---

## Phase 3 — Route Maker and Graph Processing

### Shortest paths from D (Dijkstra)
| Node | Dist | Prev |
|---|---|---|
| D | 0 | - |
| B | 2 | D |
| A | 3 | B |
| C | 8 | A |
| E | 10 | B |
| F | 13 | E |

### Nearest-neighbor TSP
Delivery set {A, B, F}.  
Route: D -> B -> A -> F -> D  
Route length: 26.0

---

## Phase 4 — Performance Testing and Optimization

| n | sort (s) | knapsack (s) | routing (s) | route len | selected |
|---|---|---|---|---|---|
| 10 | 0.000007 | 0.000102 | 0.000072 | 25.00 | 8 |
| 20 | 0.000006 | 0.000187 | 0.000152 | 61.00 | 12 |
| 40 | 0.000010 | 0.000341 | 0.000454 | 122.00 | 19 |
| 80 | 0.000027 | 0.000820 | 0.000883 | 124.00 | 22 |

Chart: outputs/runtime_chart.png

### Observations
- Sorting near-constant at small n (Timsort optimized).
- Knapsack grows linearly with n at fixed capacity (O(n*C)).
- Routing grows fastest — APSP runs Dijkstra from each delivery node.

### Future optimizations
1. Routing: 2-opt / Or-opt / Christofides; exact DP for k<20.
2. Knapsack: branch-and-bound or FPTAS for large capacity.
3. Shortest paths: cache distance matrix, use A*.
4. Parallelize independent Dijkstra runs.

---

## Phase 5 — Final Report and Demonstration

### Run
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python main.py
    python -m pytest -v

### Verified
- 6/6 unit tests pass.
- Sample: optimal priority = 11, route length = 26.
- Performance table for n = 10, 20, 40, 80.
- Runtime chart rendered.

### Evidence
screenshots/phase2_sorting_output.png  
screenshots/phase2_knapsack_output.png  
screenshots/phase3_route_output.png  
screenshots/phase4_performance_table.png  
screenshots/phase4_performance_chart.png  
screenshots/phase5_pytest_output.png

### Viva points
- Why Timsort: stable + worst-case O(n log n).
- Why 0/1 not fractional knapsack: parcels indivisible.
- Why Dijkstra fails on negative edges.
- Why NN-TSP is approximate: TSP NP-hard.
- How capacity / graph density / n affect runtime.