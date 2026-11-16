from .graph import dijkstra


def all_pairs_shortest_paths(graph, nodes):
    return {u: dijkstra(graph, u)[0] for u in nodes}


def nearest_neighbor_route(graph, depot, delivery_nodes):
    """Nearest-neighbor TSP approximation. Returns (route, total_length)."""
    if not delivery_nodes:
        return [depot], 0.0

    dist = all_pairs_shortest_paths(graph, [depot] + delivery_nodes)
    unvisited = set(delivery_nodes)
    route, cur, total = [depot], depot, 0.0

    while unvisited:
        nxt = min(unvisited, key=lambda v: dist[cur][v])
        total += dist[cur][nxt]
        route.append(nxt)
        unvisited.remove(nxt)
        cur = nxt

    total += dist[cur][depot]
    route.append(depot)
    return route, total