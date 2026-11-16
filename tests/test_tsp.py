from src.graph import load_graph_from_json
from src.tsp import nearest_neighbor_route


def test_nn_route_visits_all_and_returns():
    graph = load_graph_from_json("data/sample_graph.json")
    route, length = nearest_neighbor_route(graph, "D", ["A", "B", "F"])
    assert route[0] == "D" and route[-1] == "D"
    assert set(route[1:-1]) == {"A", "B", "F"}
    assert length == 26.0


def test_empty_delivery_returns_depot():
    graph = load_graph_from_json("data/sample_graph.json")
    route, length = nearest_neighbor_route(graph, "D", [])
    assert route == ["D"]
    assert length == 0.0