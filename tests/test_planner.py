from src.models import load_parcels_from_csv
from src.graph import load_graph_from_json
from src.planner import plan_delivery


def test_end_to_end_pipeline():
    parcels = load_parcels_from_csv("data/sample_parcels.csv")
    graph = load_graph_from_json("data/sample_graph.json")
    result = plan_delivery(parcels, capacity=8, graph=graph)

    assert result["dp"][-1][-1] == 11
    assert sum(p.weight for p in result["selected"]) <= 8
    assert result["route"][0] == "D" and result["route"][-1] == "D"
    assert result["route_length"] > 0
    assert all(k in result["times"] for k in ("sort", "knapsack", "routing"))