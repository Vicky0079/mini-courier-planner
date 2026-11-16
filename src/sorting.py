def sort_parcels(parcels):
    """Timsort O(n log n): earliest deadline first, higher priority as tie-breaker."""
    return sorted(parcels, key=lambda p: (p.deadline, -p.priority))