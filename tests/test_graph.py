from src.graph import load_graph_from_json, dijkstra


def test_dijkstra_from_depot():
    graph = load_graph_from_json("data/sample_graph.json")
    dist, prev = dijkstra(graph, "D")
    assert dist["D"] == 0
    assert dist["B"] == 2
    assert dist["A"] == 3
    assert dist["C"] == 8
    assert dist["E"] == 10
    assert dist["F"] == 13
    assert prev["A"] == "B"