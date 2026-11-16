import os
import csv

from src.models import load_parcels_from_csv
from src.graph import load_graph_from_json
from src.planner import plan_delivery
from src.performance import performance_test


def save_dp_table(dp, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(dp)


def save_route(route, length, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("Route: " + " -> ".join(route) + "\n")
        f.write(f"Total route length: {length}\n")


def save_selected(selected, path):
    with open(path, "w", encoding="utf-8") as f:
        for p in selected:
            f.write(f"{p.pid},{p.destination},{p.weight},{p.priority},{p.deadline}\n")


def save_performance(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "sort_s", "knapsack_s", "routing_s",
                    "route_length", "selected_count"])
        w.writerows(rows)


def main():
    os.makedirs("outputs", exist_ok=True)

    parcels = load_parcels_from_csv("data/sample_parcels.csv")
    graph = load_graph_from_json("data/sample_graph.json")
    capacity = 8

    result = plan_delivery(parcels, capacity, graph)

    print("=== Sorted parcels (deadline, priority) ===")
    for p in result["sorted_parcels"]:
        print(f"  {p.pid}: deadline={p.deadline}, priority={p.priority}, "
              f"weight={p.weight}, dest={p.destination}")

    print("\n=== Selected parcels (Knapsack DP) ===")
    for p in result["selected"]:
        print(f"  {p.pid} -> {p.destination}")

    print(f"\nOptimal priority value: {result['dp'][-1][-1]}")
    print("Route:", " -> ".join(result["route"]))
    print(f"Route length: {result['route_length']}")

    print("\n=== Runtime of major steps ===")
    for k, v in result["times"].items():
        print(f"  {k:9s}: {v:.6f} s")

    save_dp_table(result["dp"], "outputs/dp_table.csv")
    save_selected(result["selected"], "outputs/selected_parcels.txt")
    save_route(result["route"], result["route_length"], "outputs/route_output.txt")

    print("\n=== Performance Test (n vs runtime) ===")
    rows = performance_test()
    print(f"{'n':>4} {'sort(s)':>10} {'knap(s)':>10} {'route(s)':>10} "
          f"{'len':>8} {'sel':>4}")
    for r in rows:
        print(f"{r[0]:>4} {r[1]:>10.6f} {r[2]:>10.6f} {r[3]:>10.6f} "
              f"{r[4]:>8.2f} {r[5]:>4}")
    save_performance(rows, "outputs/performance_table.csv")

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        sizes = [r[0] for r in rows]
        plt.plot(sizes, [r[1] for r in rows], marker="o", label="Sorting")
        plt.plot(sizes, [r[2] for r in rows], marker="s", label="Knapsack DP")
        plt.plot(sizes, [r[3] for r in rows], marker="^", label="Routing")
        plt.xlabel("Number of parcels / graph size")
        plt.ylabel("Runtime (seconds)")
        plt.title("Mini-Courier Planner Runtime Comparison")
        plt.legend()
        plt.grid(True)
        plt.savefig("outputs/runtime_chart.png", dpi=120)
        print("\nSaved chart -> outputs/runtime_chart.png")
    except ImportError:
        print("\nmatplotlib not installed; skipping chart.")


if __name__ == "__main__":
    main()