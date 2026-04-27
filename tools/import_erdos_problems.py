#!/usr/bin/env python3
"""Import metadata from teorth/erdosproblems into the Magent catalog.

This adapter intentionally imports metadata only. It uses the Apache-2.0
licensed GitHub repository rather than crawling erdosproblems.com directly.

The transform is resumable: records are checkpointed as JSONL under
`.cache/imports/erdos-problems/`, and the final catalog YAML is written only
after all selected records have been transformed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only without PyYAML
    raise SystemExit(
        "PyYAML is required. Install with `python -m pip install PyYAML`."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_REPO = "https://github.com/teorth/erdosproblems.git"
DEFAULT_SOURCE_DIR = ROOT / ".cache" / "sources" / "erdosproblems"
DEFAULT_CACHE_DIR = ROOT / ".cache" / "imports" / "erdos-problems"
DEFAULT_OUTPUT = ROOT / "catalog" / "imports" / "erdos-problems" / "problems.yaml"
SOURCE_FILE_IN_REPO = Path("data") / "problems.yaml"

UNRESOLVED_STATUSES = {
    "open",
    "not provable",
    "not disprovable",
    "independent",
    "decidable",
    "falsifiable",
    "verifiable",
}

SCOPES = {
    "unresolved": UNRESOLVED_STATUSES,
    "open-only": {"open"},
    "all": None,
}


def run(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def slugify(value: str) -> str:
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unknown"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    tmp.replace(path)


def ensure_git_source(source_dir: Path, repo_url: str, no_fetch: bool) -> None:
    if shutil.which("git") is None:
        raise SystemExit("git is required to fetch teorth/erdosproblems.")

    if (source_dir / ".git").exists():
        if not no_fetch:
            run(["git", "pull", "--ff-only"], cwd=source_dir)
        return

    source_dir.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", repo_url, str(source_dir)])


def source_commit(source_dir: Path, source_file: Path) -> str | None:
    try:
        return run(["git", "rev-parse", "HEAD"], cwd=source_dir)
    except Exception:
        if ".cache" in source_file.parts:
            raise
        return None


def load_yaml_list(path: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {path}")
    return data


def normalize_prize(raw: str | None) -> dict[str, Any]:
    raw = raw or "no"
    if raw == "no":
        return {"exists": False}

    currency = "unknown"
    amount: int | None = None
    if raw.startswith("$"):
        currency = "USD"
    elif raw.startswith("\u00a3"):
        currency = "GBP"
    elif raw.startswith("\u20b9"):
        currency = "INR"

    digits = re.sub(r"[^0-9]", "", raw)
    if digits:
        amount = int(digits)

    prize: dict[str, Any] = {"exists": True, "raw": raw, "currency": currency}
    if amount is not None:
        prize["amount"] = amount
        if currency == "USD":
            prize["amount_usd"] = amount
    return prize


def normalize_oeis(values: list[str] | None) -> dict[str, Any]:
    values = values or []
    linked = [value for value in values if re.fullmatch(r"A[0-9]{6}", value or "")]
    result: dict[str, Any] = {"linked": linked}
    if "possible" in values:
        result["status"] = "possible"
    elif "N/A" in values or not values:
        result["status"] = "none"
    else:
        result["status"] = "linked" if linked else "unknown"
    return result


def formalization_for(record: dict[str, Any]) -> dict[str, Any]:
    formalized = record.get("formalized") or {}
    state = formalized.get("state", "unknown")
    result: dict[str, Any] = {"state": state, "exists": state == "yes"}
    if formalized.get("last_update"):
        result["last_update"] = formalized["last_update"]
    if state == "yes":
        number = record["number"]
        result["url"] = (
            "https://github.com/google-deepmind/formal-conjectures/blob/main/"
            f"FormalConjectures/ErdosProblems/{number}.lean"
        )
    return result


def transform_record(record: dict[str, Any]) -> dict[str, Any]:
    number = str(record["number"])
    status = (record.get("status") or {}).get("state", "unknown")
    tags = record.get("tags") or []
    area = slugify(tags[0]) if tags else "unknown"
    source_comment = record.get("comments")

    transformed: dict[str, Any] = {
        "id": f"erdos-problem-{number}",
        "title": f"Erdos Problem #{number}",
        "area": area,
        "status": status,
        "source_ids": ["erdos-problems"],
        "primary_sources": [
            {
                "title": f"Erdos Problem #{number}",
                "url": f"https://www.erdosproblems.com/{number}",
                "type": "database-record",
            },
            {
                "title": "teorth/erdosproblems data/problems.yaml",
                "url": (
                    "https://github.com/teorth/erdosproblems/blob/main/"
                    "data/problems.yaml"
                ),
                "type": "source-repository",
            },
        ],
        "introduced": {"year": "unknown", "by": []},
        "prize": normalize_prize(record.get("prize")),
        "tags": tags,
        "external_ids": {
            "erdos_number": number,
            "oeis": normalize_oeis(record.get("oeis")),
        },
        "formalization": formalization_for(record),
        "workspace_status": "not-created",
        "curation_status": "seed-only",
        "import_metadata": {
            "source_status_last_update": (record.get("status") or {}).get(
                "last_update"
            ),
        },
    }

    if source_comment:
        transformed["import_metadata"]["source_comment"] = source_comment
    if (record.get("status") or {}).get("note"):
        transformed["import_metadata"]["source_status_note"] = record["status"][
            "note"
        ]
    if (record.get("formalized") or {}).get("note"):
        transformed["formalization"]["note"] = record["formalized"]["note"]

    return transformed


def selected_records(
    records: list[dict[str, Any]], scope: str
) -> list[dict[str, Any]]:
    allowed_statuses = SCOPES[scope]
    if allowed_statuses is None:
        return records
    return [
        record
        for record in records
        if (record.get("status") or {}).get("state", "unknown") in allowed_statuses
    ]


def load_checkpoint(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}

    records: dict[str, dict[str, Any]] = {}
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            records[record["id"]] = record
    return records


def append_checkpoint(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=True))
        handle.write("\n")


def write_state(path: Path, state: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(state, indent=2, sort_keys=True) + "\n")


def write_catalog(
    output_path: Path,
    source_file: Path,
    source_hash: str,
    source_commit_hash: str | None,
    scope: str,
    source_records: list[dict[str, Any]],
    output_records: list[dict[str, Any]],
) -> None:
    status_counts = Counter(
        (record.get("status") or {}).get("state", "unknown")
        for record in source_records
    )
    output_status_counts = Counter(record["status"] for record in output_records)

    catalog = {
        "import": {
            "source_id": "erdos-problems",
            "source_name": "teorth/erdosproblems",
            "source_repository": "https://github.com/teorth/erdosproblems",
            "source_file": "data/problems.yaml",
            "source_commit": source_commit_hash or "unknown",
            "source_sha256": source_hash,
            "source_license": "Apache-2.0",
            "scope": scope,
            "imported_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
            "total_source_records": len(source_records),
            "selected_records": len(output_records),
            "source_status_counts": dict(sorted(status_counts.items())),
            "selected_status_counts": dict(sorted(output_status_counts.items())),
            "notes": [
                "Metadata-only import.",
                "Problem statements are not copied into this catalog.",
                "Use primary_sources URLs for full source context.",
            ],
        },
        "problems": output_records,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(
        catalog,
        allow_unicode=False,
        sort_keys=False,
        width=100,
    )
    atomic_write_text(output_path, text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import Erdos Problems metadata into the Magent catalog."
    )
    parser.add_argument(
        "--scope",
        choices=sorted(SCOPES),
        default="unresolved",
        help="Which source statuses to include in the output.",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Local clone of teorth/erdosproblems.",
    )
    parser.add_argument(
        "--source-file",
        type=Path,
        help="Use a local problems.yaml file instead of fetching the source repo.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Final catalog YAML output path.",
    )
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=DEFAULT_CACHE_DIR,
        help="Checkpoint directory used for resume.",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Do not clone or pull the upstream source repository.",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Discard any existing checkpoint for this source hash and scope.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit transformed records. Intended for testing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    source_file = args.source_file
    source_dir = args.source_dir
    commit_hash: str | None = None

    if source_file is None:
        ensure_git_source(source_dir, DEFAULT_SOURCE_REPO, args.no_fetch)
        source_file = source_dir / SOURCE_FILE_IN_REPO
        commit_hash = source_commit(source_dir, source_file)

    source_file = source_file.resolve()
    if not source_file.exists():
        raise SystemExit(f"Source file not found: {source_file}")

    source_hash = sha256_file(source_file)
    source_records = load_yaml_list(source_file)
    wanted = selected_records(source_records, args.scope)
    if args.limit is not None:
        wanted = wanted[: args.limit]

    cache_dir = args.cache_dir / args.scope
    checkpoint_path = cache_dir / "records.jsonl"
    state_path = cache_dir / "state.json"

    state_key = {
        "scope": args.scope,
        "source_sha256": source_hash,
        "source_file": str(source_file),
    }

    if args.fresh:
        if checkpoint_path.exists():
            checkpoint_path.unlink()
        if state_path.exists():
            state_path.unlink()

    existing_state: dict[str, Any] = {}
    if state_path.exists():
        existing_state = json.loads(state_path.read_text(encoding="utf-8"))

    if existing_state.get("source_sha256") != source_hash:
        if checkpoint_path.exists():
            checkpoint_path.unlink()
        existing_state = {}

    checkpoint_records = load_checkpoint(checkpoint_path)
    completed = set(checkpoint_records)

    for index, source_record in enumerate(wanted, start=1):
        problem_id = f"erdos-problem-{source_record['number']}"
        if problem_id in completed:
            continue

        transformed = transform_record(source_record)
        append_checkpoint(checkpoint_path, transformed)
        completed.add(problem_id)

        state = {
            **state_key,
            "completed_records": len(completed),
            "selected_records": len(wanted),
            "last_completed_id": problem_id,
            "last_completed_index": index,
            "updated_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
        }
        write_state(state_path, state)

    checkpoint_records = load_checkpoint(checkpoint_path)
    output_records = [
        checkpoint_records[f"erdos-problem-{record['number']}"]
        for record in wanted
        if f"erdos-problem-{record['number']}" in checkpoint_records
    ]

    if len(output_records) != len(wanted):
        missing = len(wanted) - len(output_records)
        raise SystemExit(f"Checkpoint incomplete: {missing} records missing")

    write_catalog(
        output_path=args.output,
        source_file=source_file,
        source_hash=source_hash,
        source_commit_hash=commit_hash,
        scope=args.scope,
        source_records=source_records,
        output_records=output_records,
    )

    print(
        f"Imported {len(output_records)} {args.scope} records "
        f"from {len(source_records)} source records into {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
