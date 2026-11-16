# Mini-Courier Planner (DAA Capstone)

## Algorithms
- Parcel prioritization: Timsort O(n log n)
- Optimal packing: 0/1 Knapsack DP O(n * capacity)
- Shortest paths: Dijkstra O((V+E) log V)
- Delivery route: Nearest-neighbor TSP approximation

## Run
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python main.py

## Outputs (in outputs/)
- dp_table.csv
- selected_parcels.txt
- route_output.txt
- performance_table.csv
- runtime_chart.png