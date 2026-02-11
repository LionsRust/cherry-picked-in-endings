#!/usr/bin/env python3
"""
Build surnames_filtered_in.json from the same CSV/txt sources as the main list.
Keeps only surnames ending in "in" (case-insensitive).

Usage:
  python3 build_in.py census.csv russian.csv
  python3 build_in.py combined.csv

Two files: first = US/combined (surname, count), second = Russian (surname, count).
One file: CSV with columns surname, count_combined, count_russian (or surname, count).
Output: surnames_filtered_in.json (in this folder).
"""

import csv
import json
import re
import sys
from pathlib import Path

def normalize(s):
    return (s or "").strip().lower()

def read_surname_count_file(path):
    """Read CSV/TSV; return dict surname -> (count_combined, count_russian)."""
    path = Path(path)
    if not path.exists():
        return {}
    out = {}
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample)
        except csv.Error:
            dialect = csv.excel
        reader = csv.reader(f, dialect)
        first = next(reader, None)
        if not first or len(first) < 2:
            return {}
        is_header = (
            first[0].strip().lower() in ("surname", "name", "lastname") or
            not re.match(r"^[\d,\.\s]+$", (first[1] or "").strip())
        )
        if is_header and len(first) >= 3:
            for row in reader:
                if len(row) < 3:
                    continue
                sn = normalize(row[0])
                if not sn:
                    continue
                try:
                    c1 = int(float(row[1].replace(",", "")))
                except (ValueError, TypeError):
                    c1 = 0
                try:
                    c2 = int(float(row[2].replace(",", "")))
                except (ValueError, TypeError):
                    c2 = 0
                out[sn] = (c1, c2)
            return out
        rows = [first] + list(reader)
    for row in rows:
        if len(row) < 2:
            continue
        sn = normalize(row[0])
        if not sn:
            continue
        try:
            c = int(float(row[1].replace(",", "")))
        except (ValueError, TypeError):
            c = 0
        out[sn] = (c, 0)
    return out

def read_census_russian(base):
    """Read surnames/Names_2010Census.csv and surnames/russian_trans_surnames.csv; return (us_dict, ru_dict)."""
    us = {}
    census_path = base / "surnames" / "Names_2010Census.csv"
    if census_path.exists():
        with open(census_path, newline="", encoding="utf-8", errors="replace") as f:
            for row in csv.DictReader(f):
                name = normalize(row.get("name", ""))
                if not name or not name.endswith("in"):
                    continue
                try:
                    us[name] = int(float((row.get("count") or "0").replace(",", "")))
                except (ValueError, TypeError):
                    us[name] = 0
    ru = {}
    ru_path = base / "surnames" / "russian_trans_surnames.csv"
    if ru_path.exists():
        with open(ru_path, newline="", encoding="utf-8", errors="replace") as f:
            for row in csv.reader(f):
                if len(row) < 2:
                    continue
                sn = normalize(row[0])
                if not sn or not sn.endswith("in"):
                    continue
                try:
                    ru[sn] = int(float((row[1] or "0").replace(",", "")))
                except (ValueError, TypeError):
                    ru[sn] = 0
    return us, ru

def main():
    base = Path(__file__).resolve().parent
    out_path = base / "surnames_filtered_in.json"

    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    if len(args) == 0:
        census_path = base / "surnames" / "Names_2010Census.csv"
        ru_path = base / "surnames" / "russian_trans_surnames.csv"
        if census_path.exists() or ru_path.exists():
            us, ru = read_census_russian(base)
            all_surnames = set(us.keys()) | set(ru.keys())
            result = []
            for s in sorted(all_surnames, key=lambda x: (-(us.get(x, 0) + ru.get(x, 0)), x)):
                result.append({
                    "surname": s,
                    "russian": ru.get(s, 0) > 0,
                    "count_combined": us.get(s, 0),
                    "count_russian": ru.get(s, 0),
                })
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(result, f, indent=0)
            print(f"Wrote {len(result)} surnames (ending in 'in') to {out_path} (from surnames/)")
            return
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=0)
        print("No input files and no surnames/ folder. Wrote empty surnames_filtered_in.json")
        print("Usage: python3 build_in.py [census.csv [russian.csv]]  OR  put CSVs in surnames/ and run with no args")
        return

    if len(args) == 1:
        combined = read_surname_count_file(args[0])
        all_surnames = {s for s in combined if s.endswith("in")}
        result = []
        for s in sorted(all_surnames, key=lambda x: (-(combined.get(x, (0, 0))[0] + combined.get(x, (0, 0))[1]), x)):
            c1, c2 = combined.get(s, (0, 0))
            result.append({
                "surname": s,
                "russian": c2 > 0,
                "count_combined": c1,
                "count_russian": c2,
            })
    else:
        census_raw = read_surname_count_file(args[0])
        russian_raw = read_surname_count_file(args[1])
        census = {s: (c1, 0) for s, (c1, _) in census_raw.items() if s.endswith("in")}
        russian = {s: (0, c2) for s, (_, c2) in russian_raw.items() if s.endswith("in")}
        all_surnames = set(census.keys()) | set(russian.keys())
        result = []
        for s in sorted(all_surnames, key=lambda x: (-(census.get(x, (0, 0))[0] + russian.get(x, (0, 0))[1]), x)):
            c1 = census.get(s, (0, 0))[0]
            c2 = russian.get(s, (0, 0))[1]
            result.append({
                "surname": s,
                "russian": c2 > 0,
                "count_combined": c1,
                "count_russian": c2,
            })

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=0)
    print(f"Wrote {len(result)} surnames (ending in 'in') to {out_path}")

if __name__ == "__main__":
    main()
