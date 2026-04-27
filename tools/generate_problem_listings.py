#!/usr/bin/env python3
"""Generate catalog-level Markdown listings for imported Erdos problems."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import unicodedata
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
DEFAULT_INPUT = ROOT / "catalog" / "imports" / "erdos-problems" / "problems.yaml"
DEFAULT_TEMPLATE = ROOT / "templates" / "problem-listing.md"
DEFAULT_OUTPUT_DIR = ROOT / "catalog" / "listings" / "erdos-problems"
DEFAULT_STATE = ROOT / ".cache" / "listings" / "erdos-problems" / "state.json"

NOTE = (
    "This is a catalog metadata listing, not a curated problem workspace. "
    "Do not treat it as a reviewed problem statement."
)


def ascii_clean(value: Any) -> str:
    text = str(value)
    replacements = {
        "\u00a3": "GBP ",
        "\u20b9": "INR ",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def atomic_write_text(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False

    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    os.replace(tmp, path)
    return True


def load_yaml_mapping(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def frontmatter_for(problem: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": problem["id"],
        "title": problem["title"],
        "area": problem.get("area", "unknown"),
        "status": problem.get("status", "unknown"),
        "source_ids": problem.get("source_ids", []),
        "workspace_status": problem.get("workspace_status", "not-created"),
        "curation_status": problem.get("curation_status", "seed-only"),
        "review": {
            "llm_reviewed": False,
            "human_reviewed": False,
            "formal_reviewed": False,
        },
    }


def yaml_block(data: Any) -> str:
    return yaml.safe_dump(
        data,
        allow_unicode=False,
        sort_keys=False,
        width=88,
    ).strip()


def list_or_none(values: list[str] | None) -> str:
    values = values or []
    return ", ".join(values) if values else "none"


def render_sources(problem: dict[str, Any]) -> str:
    sources = problem.get("primary_sources") or []
    if not sources:
        return "- none"

    lines = []
    for source in sources:
        title = source.get("title", "source")
        url = source.get("url", "")
        source_type = source.get("type", "source")
        if url:
            lines.append(f"- [{title}]({url}) ({source_type})")
        else:
            lines.append(f"- {title} ({source_type})")
    return "\n".join(lines)


def render_prize(problem: dict[str, Any]) -> str:
    prize = problem.get("prize") or {}
    if not prize.get("exists"):
        return "none listed"
    if prize.get("raw"):
        return str(prize["raw"])
    amount = prize.get("amount")
    currency = prize.get("currency", "unknown")
    return f"{amount} {currency}" if amount is not None else currency


def render_oeis(problem: dict[str, Any]) -> str:
    oeis = ((problem.get("external_ids") or {}).get("oeis")) or {}
    linked = oeis.get("linked") or []
    if not linked:
        status = oeis.get("status", "none")
        return f"none ({status})" if status != "none" else "none"
    links = [f"[{value}](https://oeis.org/{value})" for value in linked]
    status = oeis.get("status", "linked")
    return f"{', '.join(links)} ({status})"


def render_formalization(problem: dict[str, Any]) -> str:
    formalization = problem.get("formalization") or {}
    state = formalization.get("state", "unknown")
    url = formalization.get("url")
    last_update = formalization.get("last_update")
    pieces = [state]
    if url:
        pieces[0] = f"[{state}]({url})"
    if last_update:
        pieces.append(f"last update {last_update}")
    return "; ".join(pieces)


def render_listing(problem: dict[str, Any], template: str) -> str:
    frontmatter = yaml_block(frontmatter_for(problem))
    erdos_number = (problem.get("external_ids") or {}).get("erdos_number", "unknown")
    import_metadata = problem.get("import_metadata") or {}
    source_update = import_metadata.get("source_status_last_update", "unknown")
    source_comment = import_metadata.get("source_comment")

    replacements = {
        "frontmatter": frontmatter,
        "title": problem["title"],
        "note": NOTE,
        "id": problem["id"],
        "erdos_number": erdos_number,
        "area": problem.get("area", "unknown"),
        "status": problem.get("status", "unknown"),
        "workspace_status": problem.get("workspace_status", "not-created"),
        "curation_status": problem.get("curation_status", "seed-only"),
        "tags": list_or_none(problem.get("tags")),
        "prize": render_prize(problem),
        "oeis": render_oeis(problem),
        "formalization": render_formalization(problem),
        "source_update": source_update,
        "source_comment": source_comment or "none",
        "sources": render_sources(problem),
    }

    rendered = template
    for key, value in replacements.items():
        rendered = rendered.replace("{{ " + key + " }}", ascii_clean(value))
    rendered = ascii_clean(rendered).rstrip() + "\n"
    rendered.encode("ascii")
    return rendered


def sorted_problems(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    problems = catalog.get("problems")
    if not isinstance(problems, list):
        raise ValueError("Expected catalog problems list")
    return sorted(
        problems,
        key=lambda problem: int(
            (problem.get("external_ids") or {}).get("erdos_number", "0")
        ),
    )


def render_index(
    problems: list[dict[str, Any]],
    catalog_import: dict[str, Any],
) -> str:
    status_counts = Counter(problem.get("status", "unknown") for problem in problems)
    area_counts = Counter(problem.get("area", "unknown") for problem in problems)

    lines = [
        "# Erdos Problems Listings",
        "",
        NOTE,
        "",
        "Generated from `catalog/imports/erdos-problems/problems.yaml`.",
        "",
        "## Source",
        "",
        f"- Source: {catalog_import.get('source_name', 'unknown')}",
        f"- Scope: {catalog_import.get('scope', 'unknown')}",
        f"- Source commit: {catalog_import.get('source_commit', 'unknown')}",
        f"- Source SHA-256: {catalog_import.get('source_sha256', 'unknown')}",
        f"- Listings: {len(problems)}",
        "",
        "## Status Counts",
        "",
    ]

    for status, count in sorted(status_counts.items()):
        lines.append(f"- {status}: {count}")

    lines.extend(["", "## Area Counts", ""])
    for area, count in sorted(area_counts.items()):
        lines.append(f"- {area}: {count}")

    lines.extend(["", "## Entries", "", "| ID | Status | Area | Listing |", "| --- | --- | --- | --- |"])
    for problem in problems:
        problem_id = problem["id"]
        lines.append(
            "| {id} | {status} | {area} | [listing](entries/{id}.md) |".format(
                id=problem_id,
                status=problem.get("status", "unknown"),
                area=problem.get("area", "unknown"),
            )
        )

    text = "\n".join(lines).rstrip() + "\n"
    text.encode("ascii")
    return text


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_state(path: Path, state: dict[str, Any]) -> None:
    atomic_write_text(path, json.dumps(state, indent=2, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Markdown listings for imported Erdos problems."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Ignore existing listing generation state.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    catalog = load_yaml_mapping(args.input)
    problems = sorted_problems(catalog)
    template = args.template.read_text(encoding="utf-8")
    source_sha = sha256_file(args.input)
    template_sha = sha256_file(args.template)

    run_key = {
        "input": str(args.input.resolve()),
        "input_sha256": source_sha,
        "template": str(args.template.resolve()),
        "template_sha256": template_sha,
        "output_dir": str(args.output_dir.resolve()),
    }

    existing_state = {} if args.fresh else load_state(args.state)
    completed = set(existing_state.get("completed_ids", []))
    if any(existing_state.get(key) != value for key, value in run_key.items()):
        completed = set()

    entries_dir = args.output_dir / "entries"
    written = 0
    skipped = 0
    current_ids = {problem["id"] for problem in problems}

    if entries_dir.exists():
        for existing in entries_dir.glob("*.md"):
            if existing.stem not in current_ids:
                existing.unlink()
                written += 1

    for index, problem in enumerate(problems, start=1):
        problem_id = problem["id"]
        output_path = entries_dir / f"{problem_id}.md"
        if problem_id in completed and output_path.exists():
            skipped += 1
            continue

        content = render_listing(problem, template)
        if atomic_write_text(output_path, content):
            written += 1
        completed.add(problem_id)

        state = {
            **run_key,
            "completed_ids": sorted(completed),
            "completed_records": len(completed),
            "total_records": len(problems),
            "last_completed_id": problem_id,
            "last_completed_index": index,
            "updated_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
        }
        write_state(args.state, state)

    index_content = render_index(problems, catalog.get("import", {}))
    if atomic_write_text(args.output_dir / "README.md", index_content):
        written += 1

    write_state(
        args.state,
        {
            **run_key,
            "completed_ids": [problem["id"] for problem in problems],
            "completed_records": len(problems),
            "total_records": len(problems),
            "last_completed_id": problems[-1]["id"] if problems else None,
            "last_completed_index": len(problems),
            "written_files": written,
            "skipped_entries": skipped,
            "updated_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
        },
    )

    print(
        f"Generated {len(problems)} listings in {args.output_dir} "
        f"({written} files written, {skipped} entries resumed)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
