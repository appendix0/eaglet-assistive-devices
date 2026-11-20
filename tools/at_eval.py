#!/usr/bin/env python3
"""Check the project's quantitative targets against the case records.

Reads cases/<case-id>/evaluation.csv (folders starting with "_" are skipped)
and reports each target from the project plan as PASS / FAIL / PENDING.
The column definitions live in docs/evaluation.md.

Usage: python3 tools/at_eval.py [cases_dir]
Exit code: 0 = data valid (targets may still be unmet), 1 = invalid data.
"""
import csv
import re
import sys
from pathlib import Path

COLUMNS = ["timepoint", "date", "days_used", "task_done", "help_level",
           "ease", "pain_pressure", "continue_intent", "note"]
VERSION = re.compile(r"^v(\d+)$")
MIN_DAYS = 14          # plan: at least 2 weeks of real use per prototype
MIN_CASES = 3          # plan: 3 or more users / devices / published designs
KPI_RATIO = 2 / 3      # plan: 2 or more of 3 users improve


class DataError(Exception):
    pass


def _int(value, lo, hi, where, name, required=True):
    if value == "":
        if required:
            raise DataError(f"{where}: {name} is empty")
        return None
    try:
        n = int(value)
    except ValueError:
        raise DataError(f"{where}: {name}={value!r} is not a whole number")
    if not lo <= n <= hi:
        raise DataError(f"{where}: {name}={n} outside {lo}..{hi}")
    return n


def _yn(value, where, name, required=True):
    if value == "" and not required:
        return None
    if value not in ("Y", "N"):
        raise DataError(f"{where}: {name}={value!r} must be Y or N")
    return value == "Y"


def load_case(path):
    """Return {"baseline": row, "versions": [(n, row), ...]} for one CSV."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != COLUMNS:
            raise DataError(f"{path}: header must be {','.join(COLUMNS)}")
        baseline, versions = None, []
        for line, raw in enumerate(reader, start=2):
            where = f"{path}:{line}"
            tp = raw["timepoint"].strip()
            is_base = tp == "baseline"
            m = VERSION.match(tp)
            if not (is_base or m):
                raise DataError(f"{where}: timepoint {tp!r} must be baseline or v1, v2, ...")
            row = {
                "task_done": _yn(raw["task_done"].strip(), where, "task_done"),
                "help_level": _int(raw["help_level"].strip(), 0, 4, where, "help_level"),
                "days_used": _int(raw["days_used"].strip(), 0, 3650, where,
                                  "days_used", required=not is_base),
                "ease": _int(raw["ease"].strip(), 1, 5, where, "ease", required=not is_base),
                "pain_pressure": _yn(raw["pain_pressure"].strip(), where,
                                     "pain_pressure", required=not is_base),
                "continue_intent": _int(raw["continue_intent"].strip(), 1, 5, where,
                                        "continue_intent", required=not is_base),
            }
            if is_base:
                if baseline is not None:
                    raise DataError(f"{where}: second baseline row")
                baseline = row
            else:
                versions.append((int(m.group(1)), row))
    nums = [n for n, _ in versions]
    if len(nums) != len(set(nums)):
        raise DataError(f"{path}: duplicate version timepoint")
    return {"baseline": baseline, "versions": sorted(versions, key=lambda v: v[0])}


def improved(case):
    """Plan KPI: target task newly possible, or less help needed than at baseline."""
    base, versions = case["baseline"], case["versions"]
    if base is None or not versions:
        return None
    final = versions[-1][1]
    newly_done = (not base["task_done"]) and final["task_done"]
    less_help = final["help_level"] < base["help_level"]
    return newly_done or less_help


def evaluate(cases_dir):
    cases_dir = Path(cases_dir)
    cases = {}
    for d in sorted(p for p in cases_dir.iterdir() if p.is_dir() and not p.name.startswith("_")):
        csv_path = d / "evaluation.csv"
        if csv_path.exists():
            c = load_case(csv_path)
            c["published"] = any((d / "stl").glob("*.stl"))
            cases[d.name] = c
    return cases


def targets(cases):
    """Return [(name, status, detail)] with status PASS / FAIL / PENDING."""
    out = []
    enrolled = [k for k, c in cases.items() if c["baseline"] is not None]
    out.append(("users with a baseline record >= 3",
                "PASS" if len(enrolled) >= MIN_CASES else "PENDING", f"{len(enrolled)}"))

    def per_case(name, ok):
        results = {k: ok(c) for k, c in cases.items() if c["baseline"] is not None}
        bad = [k for k, v in results.items() if v is False]
        waiting = [k for k, v in results.items() if v is None]
        if bad:
            status = "FAIL"
        elif waiting or len(results) < MIN_CASES:
            status = "PENDING"
        else:
            status = "PASS"
        detail = ", ".join(f"{k}={'-' if v is None else ('ok' if v else 'NO')}"
                           for k, v in results.items())
        out.append((name, status, detail or "no cases"))

    def first_use_long_enough(c):
        v1 = dict(c["versions"]).get(1)
        return None if v1 is None else v1["days_used"] >= MIN_DAYS

    def revised(c):
        return True if len(c["versions"]) >= 2 else None

    per_case(f"v1 used >= {MIN_DAYS} days", first_use_long_enough)
    per_case("at least 1 revision (v2+)", revised)

    scored = {k: improved(c) for k, c in cases.items()}
    scored = {k: v for k, v in scored.items() if v is not None}
    n_imp = sum(scored.values())
    if len(scored) < MIN_CASES:
        status = "PENDING"
    else:
        status = "PASS" if n_imp / len(scored) >= KPI_RATIO else "FAIL"
    out.append(("KPI: improved users >= 2/3", status, f"{n_imp}/{len(scored)} improved"))

    pub = sum(c["published"] for c in cases.values())
    out.append(("published designs (stl/) >= 3",
                "PASS" if pub >= MIN_CASES else "PENDING", f"{pub}"))
    return out


def main(argv):
    cases_dir = argv[1] if len(argv) > 1 else Path(__file__).resolve().parent.parent / "cases"
    try:
        cases = evaluate(cases_dir)
    except DataError as e:
        print(f"invalid data: {e}", file=sys.stderr)
        return 1
    for name, status, detail in targets(cases):
        print(f"{status:8} {name:40} {detail}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
