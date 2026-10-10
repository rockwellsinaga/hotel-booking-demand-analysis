import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path


LEAD_TIME_BINS = (
    ("0-7", 0, 7),
    ("8-30", 8, 30),
    ("31-90", 31, 90),
    ("91-180", 91, 180),
    ("181-365", 181, 365),
    (">365", 366, float("inf")),
)


def rate(canceled, total):
    return canceled / total if total else None


def summarize(rows):
    resort_rows = [row for row in rows if row.get("hotel") == "Resort Hotel"]
    totals = Counter(int(row["is_canceled"]) for row in resort_rows)
    by_year = defaultdict(Counter)
    by_customer_type = defaultdict(Counter)
    by_channel = defaultdict(Counter)
    repeated_by_channel = defaultdict(Counter)
    by_lead_time = defaultdict(Counter)

    for row in resort_rows:
        canceled = int(row["is_canceled"])
        by_year[row["arrival_date_year"]][canceled] += 1
        by_customer_type[row["customer_type"]][canceled] += 1
        by_channel[row["distribution_channel"]][canceled] += 1
        repeated_by_channel[row["distribution_channel"]][int(row["is_repeated_guest"])] += 1
        lead_time = int(row["lead_time"])
        for label, lower, upper in LEAD_TIME_BINS:
            if lower <= lead_time <= upper:
                by_lead_time[label][canceled] += 1
                break

    def render(groups):
        return {
            key: {
                "bookings": counts[0] + counts[1],
                "canceled": counts[1],
                "not_canceled": counts[0],
                "cancellation_rate": rate(counts[1], counts[0] + counts[1]),
            }
            for key, counts in sorted(groups.items())
        }

    total = totals[0] + totals[1]
    return {
        "scope": "Resort Hotel only",
        "bookings": total,
        "canceled": totals[1],
        "not_canceled": totals[0],
        "cancellation_rate": rate(totals[1], total),
        "by_year": render(by_year),
        "by_customer_type": render(by_customer_type),
        "by_distribution_channel": render(by_channel),
        "repeated_guest_by_distribution_channel": {
            key: {
                "bookings": counts[0] + counts[1],
                "repeated_guest_bookings": counts[1],
                "repeated_guest_rate": rate(counts[1], counts[0] + counts[1]),
            }
            for key, counts in sorted(repeated_by_channel.items())
        },
        "by_lead_time": render(by_lead_time),
    }


def main():
    parser = argparse.ArgumentParser(description="Reproduce Resort Hotel cancellation metrics.")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    with args.csv_path.open(encoding="utf-8-sig", newline="") as source:
        result = summarize(csv.DictReader(source))
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
