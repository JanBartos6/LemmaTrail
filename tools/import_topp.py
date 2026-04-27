#!/usr/bin/env python3
"""Import metadata from TOPP into the LemmaTrail catalog.

This adapter imports metadata only from the public TOPP Git repository. It
does not copy problem statements, origins, status prose, or related results.

The transform is resumable: records are checkpointed as JSONL under
`.cache/imports/topp/`, and the final catalog YAML is written only after all
selected records have been transformed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
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
DEFAULT_SOURCE_REPO = "https://github.com/edemaine/topp.git"
DEFAULT_SOURCE_DIR = ROOT / ".cache" / "sources" / "topp"
DEFAULT_CACHE_DIR = ROOT / ".cache" / "imports" / "topp"
DEFAULT_OUTPUT = ROOT / "catalog" / "imports" / "topp" / "problems.yaml"
PROBLEM_DIR_IN_REPO = Path("Problems")

SCOPES = {
    "unresolved": {"open", "partially-resolved", "unknown"},
    "all": None,
}

FIELD_RE = re.compile(r"^\*\s*([^:]+):\s*(.*)$")
SEPARATOR_RE = re.compile(r"^-+\s*$")
NONE_RE = re.compile(r"^<none>$", re.IGNORECASE)


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


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    tmp.replace(path)


def sha256_paths(paths: list[Path], root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(str(path.relative_to(root)).replace("\\", "/").encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def ensure_git_source(source_dir: Path, repo_url: str, no_fetch: bool) -> None:
    if shutil.which("git") is None:
        raise SystemExit("git is required to fetch edemaine/topp.")

    if (source_dir / ".git").exists():
        if not no_fetch:
            run(["git", "pull", "--ff-only"], cwd=source_dir)
        return

    source_dir.parent.mkdir(parents=True, exist_ok=True)
    run(["git", "clone", "--depth", "1", repo_url, str(source_dir)])


def source_commit(source_dir: Path) -> str:
    return run(["git", "rev-parse", "HEAD"], cwd=source_dir)


def clean_lines(lines: list[str]) -> list[str]:
    while lines and not lines[0].strip():
        del lines[0]
    while lines and not lines[-1].strip():
        del lines[-1]
    return lines


def flatten(lines: list[str] | None) -> str:
    if not lines:
        return ""
    return " ".join(" ".join(line.split()) for line in lines if line.strip()).strip()


def parse_categories(lines: list[str] | None) -> list[str]:
    text = flatten(lines)
    if not text:
        return []
    parts = re.split(r"[;,]", text)
    return [part.strip().rstrip(".") for part in parts if part.strip().rstrip(".")]


def parse_problem_file(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    record: dict[str, Any] = {"fields": []}
    current_field: str | None = None

    def finish_record() -> None:
        nonlocal record
        for key, value in list(record.items()):
            if isinstance(value, list):
                record[key] = clean_lines(value)
        if "Number" in record and "Problem" in record:
            record["source_file"] = path
            records.append(record)
        record = {"fields": []}

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if SEPARATOR_RE.match(line):
            finish_record()
            current_field = None
            continue

        match = FIELD_RE.match(line)
        if match:
            field = match.group(1).strip()
            value = match.group(2).strip()
            current_field = field
            if NONE_RE.match(value):
                continue
            if field == "Number":
                record[field] = int(value)
            elif field == "Problem":
                record[field] = value
            else:
                record["fields"].append(field)
                record[field] = [value]
            continue

        if current_field and current_field in record:
            value = record[current_field]
            if isinstance(value, list):
                value.append(line)

    finish_record()
    return records


def load_source_records(problem_dir: Path) -> list[dict[str, Any]]:
    paths = sorted(problem_dir.glob("P.[0-9][0-9][0-9][0-9][0-9][0-9]"))
    records: list[dict[str, Any]] = []
    for path in paths:
        records.extend(parse_problem_file(path))
    return sorted(records, key=lambda record: record["Number"])


def infer_status(record: dict[str, Any]) -> str:
    status_fields = [
        field for field in record.get("fields", []) if "status" in field.lower()
    ]
    text = " ".join(flatten(record.get(field)) for field in status_fields).lower()
    if not text:
        return "unknown"

    solved_like = any(word in text for word in ["solved", "closed", "settled"])
    open_like = any(
        phrase in text
        for phrase in [
            "open",
            "remains open",
            "remain open",
            "question remains",
            "still unknown",
        ]
    )
    partial_like = "partial" in text or "partially" in text

    if solved_like and (open_like or partial_like):
        return "partially-resolved"
    if solved_like:
        return "solved"
    if open_like:
        return "open"
    return "unknown"


def selected_records(records: list[dict[str, Any]], scope: str) -> list[dict[str, Any]]:
    allowed_statuses = SCOPES[scope]
    if allowed_statuses is None:
        return records
    return [
        record
        for record in records
        if infer_status(record) in allowed_statuses
    ]


def transform_record(record: dict[str, Any], source_root: Path) -> dict[str, Any]:
    number = int(record["Number"])
    categories = parse_categories(record.get("Categories"))
    source_file = record["source_file"]
    relative_source_file = source_file.relative_to(source_root).as_posix()
    status_fields = [
        field for field in record.get("fields", []) if "status" in field.lower()
    ]

    transformed: dict[str, Any] = {
        "id": f"topp-problem-{number}",
        "title": record["Problem"],
        "area": "computational-geometry",
        "status": infer_status(record),
        "source_ids": ["topp"],
        "primary_sources": [
            {
                "title": f"TOPP Problem {number}",
                "url": f"https://topp.openproblem.net/P{number}.html",
                "type": "database-record",
            },
            {
                "title": f"edemaine/topp {relative_source_file}",
                "url": (
                    "https://github.com/edemaine/topp/blob/main/"
                    f"{relative_source_file}"
                ),
                "type": "source-repository",
            },
        ],
        "introduced": {"year": "unknown", "by": []},
        "prize": {"exists": bool(record.get("Reward"))},
        "tags": categories,
        "external_ids": {"topp_number": str(number)},
        "workspace_status": "not-created",
        "curation_status": "seed-only",
        "import_metadata": {
            "source_file": relative_source_file,
            "source_fields": record.get("fields", []),
            "status_source_fields": status_fields,
            "status_inference": "keyword-only; verify against source before curation",
        },
    }

    if categories:
        transformed["area"] = slugify(categories[0])

    return transformed


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
    source_root: Path,
    source_hash: str,
    source_commit_hash: str,
    scope: str,
    source_records: list[dict[str, Any]],
    output_records: list[dict[str, Any]],
) -> None:
    source_status_counts = Counter(infer_status(record) for record in source_records)
    output_status_counts = Counter(record["status"] for record in output_records)
    catalog = {
        "import": {
            "source_id": "topp",
            "source_name": "TOPP - The Open Problems Project",
            "source_repository": "https://github.com/edemaine/topp",
            "source_commit": source_commit_hash,
            "source_sha256": source_hash,
            "source_license": "mixed-or-unclear-for-problem-text",
            "scope": scope,
            "imported_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
            "total_source_records": len(source_records),
            "selected_records": len(output_records),
            "source_status_counts": dict(sorted(source_status_counts.items())),
            "selected_status_counts": dict(sorted(output_status_counts.items())),
            "notes": [
                "Metadata-only import.",
                "Problem statements and status prose are not copied into this catalog.",
                "Status is inferred from short source status fields and must be rechecked.",
                "Use primary_sources URLs for full source context.",
            ],
        },
        "problems": output_records,
    }

    text = yaml.safe_dump(catalog, allow_unicode=False, sort_keys=False, width=100)
    atomic_write_text(output_path, text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import TOPP metadata into the LemmaTrail catalog."
    )
    parser.add_argument(
        "--scope",
        choices=sorted(SCOPES),
        default="unresolved",
        help="Which inferred source statuses to include in the output.",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Local clone of edemaine/topp.",
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

    ensure_git_source(args.source_dir, DEFAULT_SOURCE_REPO, args.no_fetch)
    source_root = args.source_dir.resolve()
    problem_dir = source_root / PROBLEM_DIR_IN_REPO
    if not problem_dir.exists():
        raise SystemExit(f"TOPP problem directory not found: {problem_dir}")

    problem_paths = sorted(problem_dir.glob("P.[0-9][0-9][0-9][0-9][0-9][0-9]"))
    source_hash = sha256_paths(problem_paths, source_root)
    commit_hash = source_commit(source_root)
    source_records = load_source_records(problem_dir)
    wanted = selected_records(source_records, args.scope)
    if args.limit is not None:
        wanted = wanted[: args.limit]

    cache_dir = args.cache_dir / args.scope
    checkpoint_path = cache_dir / "records.jsonl"
    state_path = cache_dir / "state.json"
    state_key = {
        "scope": args.scope,
        "source_sha256": source_hash,
        "source_dir": str(source_root),
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

    checkpoint_records = load_checkpoint(checkpoint_path)
    completed = set(checkpoint_records)

    for index, source_record in enumerate(wanted, start=1):
        problem_id = f"topp-problem-{source_record['Number']}"
        if problem_id in completed:
            continue

        transformed = transform_record(source_record, source_root)
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
        checkpoint_records[f"topp-problem-{record['Number']}"]
        for record in wanted
        if f"topp-problem-{record['Number']}" in checkpoint_records
    ]
    if len(output_records) != len(wanted):
        missing = len(wanted) - len(output_records)
        raise SystemExit(f"Checkpoint incomplete: {missing} records missing")

    write_catalog(
        output_path=args.output,
        source_root=source_root,
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
