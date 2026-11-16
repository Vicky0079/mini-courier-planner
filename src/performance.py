import random
from .models import Parcel
from .planner import plan_delivery


def generate_random_graph(num_nodes, extra_edges=2, seed=0):
    rng = random.Random(seed)
    nodes = ["D"] + [f"N{i}" for i in range(1, num_nodes)]
    graph = {n: [] for n in nodes}

    def add(u, v, w):
        graph[u].append((v, w))
        graph[v].append((u, w))

    for i in range(len(nodes)):
        add(nodes[i], nodes[(i + 1) % len(nodes)], rng.randint(1, 20))
    for _ in range(extra_edges * num_nodes):
        u, v = rng.sample(nodes, 2)
        add(u, v, rng.randint(1, 20))
    return graph, nodes


def generate_parcels(num_parcels, nodes, seed=0):
    rng = random.Random(seed)
    dests = [n for n in nodes if n != "D"]
    return [Parcel(f"P{i+1}", rng.randint(1, 10), rng.randint(1, 5),
                   rng.randint(1, 24), rng.choice(dests))
            for i in range(num_parcels)]


def performance_test(sizes=(10, 20, 40, 80), capacity=50):
    rows = []
    for n in sizes:
        graph, nodes = generate_random_graph(max(5, n // 2), seed=n)
        parcels = generate_parcels(n, nodes, seed=n)
        r = plan_delivery(parcels, capacity, graph)
        t = r["times"]
        rows.append([n, t["sort"], t["knapsack"], t["routing"],
                     round(r["route_length"], 2), len(r["selected"])])
    return rows