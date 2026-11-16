from src.models import Parcel
from src.sorting import sort_parcels


def test_sort_by_deadline_then_priority():
    parcels = [
        Parcel("P1", 3, 5, 5, "A"),
        Parcel("P2", 4, 4, 3, "B"),
        Parcel("P3", 2, 3, 8, "C"),
        Parcel("P4", 5, 5, 2, "E"),
        Parcel("P5", 1, 2, 6, "F"),
    ]
    order = [p.pid for p in sort_parcels(parcels)]
    assert order == ["P4", "P2", "P1", "P5", "P3"]