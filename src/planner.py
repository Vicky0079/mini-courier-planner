import time
from .sorting import sort_parcels
from .knapsack import knapsack
from .tsp import nearest_neighbor_route


def plan_delivery(parcels, capacity, graph, depot="D"):
    t0 = time.perf_counter()
    sorted_parcels = sort_parcels(parcels)
    t1 = time.perf_counter()

    selected, dp = knapsack(sorted_parcels, capacity)
    t2 = time.perf_counter()

    delivery_nodes = list(dict.fromkeys(p.destination for p in selected))
    route, route_length = nearest_neighbor_route(graph, depot, delivery_nodes)
    t3 = time.perf_counter()

    return {
        "sorted_parcels": sorted_parcels,
        "selected": selected,
        "dp": dp,
        "route": route,
        "route_length": route_length,
        "times": {"sort": t1 - t0, "knapsack": t2 - t1, "routing": t3 - t2},
    }