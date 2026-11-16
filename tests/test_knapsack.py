from src.models import Parcel
from src.knapsack import knapsack


def test_knapsack_optimal_value_and_capacity():
    parcels = [
        Parcel("P4", 5, 5, 2, "E"),
        Parcel("P2", 4, 4, 3, "B"),
        Parcel("P1", 3, 5, 5, "A"),
        Parcel("P5", 1, 2, 6, "F"),
        Parcel("P3", 2, 3, 8, "C"),
    ]
    selected, dp = knapsack(parcels, capacity=8)
    assert dp[-1][-1] == 11
    assert sum(p.weight for p in selected) <= 8
    assert sorted(p.pid for p in selected) == ["P1", "P2", "P5"]