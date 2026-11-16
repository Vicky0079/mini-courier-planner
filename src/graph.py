import heapq
import json


def add_edge(graph, u, v, w):
    graph.setdefault(u, []).append((v, w))
    graph.setdefault(v, []).append((u, w))


def load_graph_from_json(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    graph = {n: [] for n in data["nodes"]}
    for u, v, w in data["edges"]:
        add_edge(graph, u, v, w)
    return graph


def dijkstra(graph, start):
    dist = {n: float("inf") for n in graph}
    prev = {n: None for n in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev