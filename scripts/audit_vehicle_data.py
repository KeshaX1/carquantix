import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from car_data import load_cars


REQUIRED_AUDIT_FIELDS = (
    "modelYear",
    "trim",
    "bodyStyle",
    "priceMarket",
    "measurementStandard",
    "sourceName",
    "sourceUrl",
    "verifiedAt",
)

REQUIRED_DIMENSION_FIELDS = ("length", "width", "weight")


def missing_fields(car):
    audit = car.get("dataAudit") or {}
    dimensions = car.get("dimensions") or {}
    missing = [f"dataAudit.{field}" for field in REQUIRED_AUDIT_FIELDS if not audit.get(field)]
    missing.extend(
        f"dimensions.{field}"
        for field in REQUIRED_DIMENSION_FIELDS
        if dimensions.get(field) is None
    )
    return missing


def main():
    cars, _ = load_cars()
    incomplete = []
    for car in cars:
        missing = missing_fields(car)
        if missing:
            incomplete.append((car.get("id") or car.get("name") or "unknown", car.get("name") or "", missing))

    print(f"Cars checked: {len(cars)}")
    print(f"Complete records: {len(cars) - len(incomplete)}")
    print(f"Incomplete records: {len(incomplete)}")
    for car_id, name, missing in incomplete[:80]:
        print(f"- {car_id} | {name}: {', '.join(missing)}")
    if len(incomplete) > 80:
        print(f"... {len(incomplete) - 80} more incomplete records")


if __name__ == "__main__":
    main()
