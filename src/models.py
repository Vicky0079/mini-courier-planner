from dataclasses import dataclass
import csv


@dataclass
class Parcel:
    pid: str
    weight: int
    priority: int
    deadline: int
    destination: str


def load_parcels_from_csv(path):
    parcels = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            parcels.append(Parcel(
                pid=row["pid"],
                weight=int(row["weight"]),
                priority=int(row["priority"]),
                deadline=int(row["deadline"]),
                destination=row["destination"],
            ))
    return parcels


def save_parcels_to_csv(parcels, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pid", "weight", "priority", "deadline", "destination"])
        for p in parcels:
            w.writerow([p.pid, p.weight, p.priority, p.deadline, p.destination])