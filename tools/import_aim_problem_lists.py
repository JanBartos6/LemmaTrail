#!/usr/bin/env python3
"""Import AIM Problem Lists link metadata into the Magent catalog.

This adapter imports the AIM list-of-lists only. It does not crawl AIMPL pages,
download PDFs, or copy problem statements.

The transform is resumable: records are checkpointed as JSONL under
`.cache/imports/aim-problem-lists/`, and the final catalog YAML is written only
after all selected records have been transformed.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import urllib.robotparser
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only without PyYAML
    raise SystemExit(
        "PyYAML is required. Install with `python -m pip install PyYAML`."
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_URL = "https://aimath.org/problemlists/"
DEFAULT_CACHE_DIR = ROOT / ".cache" / "imports" / "aim-problem-lists"
DEFAULT_OUTPUT = (
    ROOT / "catalog" / "imports" / "aim-problem-lists" / "problem-lists.yaml"
)
DEFAULT_USER_AGENT = "Magent metadata importer"

SKIP_AREAS = {
    "",
    "Main menu",
}

SKIP_TITLES = {
    "National Science Foundation",
    "NSF Mathematical Sciences Institutes.",
}


def slugify(value: str) -> str:
    value = html.unescape(value).lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "unknown"


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8", newline="\n")
    tmp.replace(path)


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def normalize_space(value: str) -> str:
    return " ".join(html.unescape(value).split())


def fetch_text(url: str, user_agent: str) -> str:
    request = Request(url, headers={"User-Agent": user_agent})
    with urlopen(request, timeout=60) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, "replace")


def robots_allowed(url: str, user_agent: str) -> bool | str:
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    parser = urllib.robotparser.RobotFileParser()
    try:
        robots_text = fetch_text(robots_url, user_agent)
        parser.parse(robots_text.splitlines())
    except Exception:
        return "unknown"
    return parser.can_fetch(user_agent, url)


class AimProblemListsParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self.base_url = base_url
        self.area: str | None = None
        self.in_h3 = False
        self.in_a = False
        self.href: str | None = None
        self.buffer: list[str] = []
        self.links: list[dict[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag == "h3":
            self.in_h3 = True
            self.buffer = []
        elif tag == "a" and self.area:
            self.in_a = True
            self.href = attrs_dict.get("href")
            self.buffer = []

    def handle_data(self, data: str) -> None:
        if self.in_h3 or self.in_a:
            self.buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h3" and self.in_h3:
            self.area = normalize_space("".join(self.buffer))
            self.in_h3 = False
            self.buffer = []
        elif tag == "a" and self.in_a:
            title = normalize_space("".join(self.buffer))
            if self.href and title:
                url, _fragment = urldefrag(urljoin(self.base_url, self.href.strip()))
                url = url.strip()
                self.links.append(
                    {
                        "title": title,
                        "url": url,
                        "source_area": self.area or "unknown",
                    }
                )
            self.in_a = False
            self.href = None
            self.buffer = []


def source_kind(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if host.endswith("aimpl.org"):
        return "aimpl"
    if path.endswith(".pdf"):
        return "pdf"
    if host == "github.com" or host.endswith(".github.com"):
        return "source-repository"
    if host == "www.overleaf.com" or host == "overleaf.com":
        return "source-document"
    if host == "sites.google.com":
        return "external-problem-list"
    if host.endswith("aimath.org"):
        return "aim-page"
    return "unknown"


def source_type(kind: str) -> str:
    return {
        "aimpl": "database-record",
        "pdf": "paper",
        "source-repository": "source-repository",
        "source-document": "source-document",
        "external-problem-list": "external-index",
        "aim-page": "database-record",
    }.get(kind, "unknown")


def parse_links(source_html: str, source_url: str) -> list[dict[str, Any]]:
    parser = AimProblemListsParser(source_url)
    parser.feed(source_html)

    by_url: dict[str, dict[str, Any]] = {}
    for link in parser.links:
        area = link["source_area"]
        title = link["title"]
        url = link["url"]
        kind = source_kind(url)
        if area in SKIP_AREAS or title in SKIP_TITLES or kind == "unknown":
            continue
        if url.rstrip("/") == source_url.rstrip("/"):
            continue

        if url not in by_url:
            by_url[url] = {
                "title": title,
                "url": url,
                "source_kind": kind,
                "source_areas": [area],
            }
        elif area not in by_url[url]["source_areas"]:
            by_url[url]["source_areas"].append(area)

    return list(by_url.values())


def make_unique_id(base: str, used: set[str]) -> str:
    candidate = base
    index = 2
    while candidate in used:
        candidate = f"{base}-{index}"
        index += 1
    used.add(candidate)
    return candidate


def transform_links(links: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    used_ids: set[str] = set()

    for link in links:
        areas = link["source_areas"]
        area_slug = slugify(areas[0]) if areas else "unknown"
        record_id = make_unique_id(f"aim-list-{slugify(link['title'])}", used_ids)

        records.append(
            {
                "id": record_id,
                "title": link["title"],
                "area": area_slug,
                "status": "unknown",
                "source_ids": ["aim-problem-lists"],
                "primary_sources": [
                    {
                        "title": link["title"],
                        "url": link["url"],
                        "type": source_type(link["source_kind"]),
                    }
                ],
                "source_kind": link["source_kind"],
                "workspace_status": "not-created",
                "curation_status": "seed-only",
                "import_metadata": {
                    "source_areas": areas,
                    "list_index_only": True,
                },
            }
        )

    return records


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
    source_url: str,
    source_hash: str,
    source_records: list[dict[str, Any]],
    output_records: list[dict[str, Any]],
    robots_result: bool | str,
) -> None:
    kind_counts = Counter(record["source_kind"] for record in output_records)
    area_counts = Counter(record["area"] for record in output_records)

    catalog = {
        "import": {
            "source_id": "aim-problem-lists",
            "source_name": "American Institute of Mathematics - Problem Lists",
            "source_url": source_url,
            "source_sha256": source_hash,
            "source_license": "unknown",
            "imported_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
            "total_source_links": len(source_records),
            "selected_records": len(output_records),
            "source_kind_counts": dict(sorted(kind_counts.items())),
            "area_counts": dict(sorted(area_counts.items())),
            "robots_allowed": robots_result,
            "notes": [
                "Metadata-only list index.",
                "AIMPL pages and PDFs are not crawled or copied.",
                "Records are source lists, not individual curated problems.",
                "Use primary_sources URLs for full source context.",
            ],
        },
        "problem_lists": output_records,
    }

    text = yaml.safe_dump(catalog, allow_unicode=False, sort_keys=False, width=100)
    atomic_write_text(output_path, text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import AIM Problem Lists link metadata into the Magent catalog."
    )
    parser.add_argument(
        "--source-url",
        default=DEFAULT_SOURCE_URL,
        help="AIM problem lists index URL.",
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
        "--user-agent",
        default=DEFAULT_USER_AGENT,
        help="User agent used for fetching the index page.",
    )
    parser.add_argument(
        "--fresh",
        action="store_true",
        help="Discard any existing checkpoint for this source hash.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Limit transformed records. Intended for testing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    robots_result = robots_allowed(args.source_url, args.user_agent)
    if robots_result is False:
        raise SystemExit(f"robots.txt does not allow fetching {args.source_url}")

    source_html = fetch_text(args.source_url, args.user_agent)
    source_hash = sha256_text(source_html)
    source_records = parse_links(source_html, args.source_url)
    transformed_records = transform_links(source_records)
    if args.limit is not None:
        transformed_records = transformed_records[: args.limit]

    cache_dir = args.cache_dir / "all"
    checkpoint_path = cache_dir / "records.jsonl"
    state_path = cache_dir / "state.json"
    state_key = {
        "source_url": args.source_url,
        "source_sha256": source_hash,
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

    for index, record in enumerate(transformed_records, start=1):
        if record["id"] in completed:
            continue

        append_checkpoint(checkpoint_path, record)
        completed.add(record["id"])
        state = {
            **state_key,
            "completed_records": len(completed),
            "selected_records": len(transformed_records),
            "last_completed_id": record["id"],
            "last_completed_index": index,
            "updated_at": dt.datetime.now(dt.timezone.utc)
            .replace(microsecond=0)
            .isoformat(),
        }
        write_state(state_path, state)

    checkpoint_records = load_checkpoint(checkpoint_path)
    output_records = [
        checkpoint_records[record["id"]]
        for record in transformed_records
        if record["id"] in checkpoint_records
    ]
    if len(output_records) != len(transformed_records):
        missing = len(transformed_records) - len(output_records)
        raise SystemExit(f"Checkpoint incomplete: {missing} records missing")

    write_catalog(
        output_path=args.output,
        source_url=args.source_url,
        source_hash=source_hash,
        source_records=source_records,
        output_records=output_records,
        robots_result=robots_result,
    )

    print(
        f"Imported {len(output_records)} AIM list records "
        f"from {len(source_records)} source links into {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
