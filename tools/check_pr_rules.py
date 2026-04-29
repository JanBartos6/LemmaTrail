#!/usr/bin/env python3
"""Check PR shape rules for LemmaTrail.

This guard does not review mathematics. It only checks whether a PR is shaped
like something maintainers are willing to review.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any


TECHNICAL_LABELS = {"type: technical", "technical"}
RESEARCH_LABELS = {"type: research", "research"}
OVERRIDE_LABELS = {"maintainer-override", "pr-guard: override"}

ALLOWED_STATUSES = {
    "idea",
    "proposed",
    "triaged",
    "needs-review",
    "verified",
    "formally-verified",
    "refuted",
    "blocked",
    "superseded",
}

RESEARCH_OBJECT_RE = re.compile(
    r"^problems/[^/]+/(problem\.md|tasks\.md|proposals/.+\.md|review/.+\.md|refuted/.+\.md)$"
)
RESEARCH_SUPPORT_RE = re.compile(
    r"^problems/[^/]+/(graph\.yaml|references\.bib)$"
)
PROBLEM_PATH_RE = re.compile(r"^problems/([^/]+)/")

TECHNICAL_ALLOWED_ROOT_FILES = {
    ".gitattributes",
    ".gitignore",
    "AGENTS.md",
    "CONTRIBUTING.md",
    "INSTRUCTIONS.md",
    "LICENSE-CODE.md",
    "LICENSE-CONTENT.md",
    "LICENSE.md",
    "MODEL_PROMPT.md",
    "README.md",
    "REVIEW_GUIDE.md",
    "requirements.txt",
}
TECHNICAL_ALLOWED_PREFIXES = (
    ".github/",
    "catalog/",
    "docs/",
    "templates/",
    "tools/",
    "problems/_template/",
)

BLOCKED_BINARY_EXTENSIONS = {
    ".7z",
    ".avi",
    ".doc",
    ".docx",
    ".gif",
    ".gz",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp4",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".tar",
    ".webp",
    ".xls",
    ".xlsx",
    ".zip",
}

RAW_TRANSCRIPT_RE = re.compile(
    r"^\s*(user|assistant|chatgpt|claude|gemini|system)\s*:", re.IGNORECASE
)
REVIEW_TRUE_RE = re.compile(
    r"^\s*(llm_reviewed|human_reviewed|formal_reviewed)\s*:\s*true\s*$",
    re.IGNORECASE,
)

MAX_REGULAR_FILE_BYTES = 120_000
MAX_CATALOG_IMPORT_BYTES = 2_000_000


@dataclass
class ChangedFile:
    status: str
    path: str
    old_path: str | None = None


def run_git(args: list[str]) -> bytes:
    result = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def normalize_path(path: str) -> str:
    return path.replace("\\", "/")


def parse_name_status(raw: bytes) -> list[ChangedFile]:
    parts = raw.decode("utf-8", "replace").split("\0")
    if parts and parts[-1] == "":
        parts.pop()

    changed: list[ChangedFile] = []
    index = 0
    while index < len(parts):
        status = parts[index]
        index += 1
        if not status:
            continue
        code = status[0]
        if code in {"R", "C"}:
            old_path = normalize_path(parts[index])
            new_path = normalize_path(parts[index + 1])
            index += 2
            changed.append(ChangedFile(status=code, path=new_path, old_path=old_path))
        else:
            path = normalize_path(parts[index])
            index += 1
            changed.append(ChangedFile(status=code, path=path))
    return changed


def changed_files(rev_range: str) -> list[ChangedFile]:
    raw = run_git(["diff", "--name-status", "--find-renames", "-z", rev_range])
    return parse_name_status(raw)


def head_revision(rev_range: str) -> str:
    if "..." in rev_range:
        return rev_range.rsplit("...", 1)[1] or "HEAD"
    if ".." in rev_range:
        return rev_range.rsplit("..", 1)[1] or "HEAD"
    return "HEAD"


def file_bytes_at(revision: str, path: str) -> bytes | None:
    try:
        return run_git(["show", f"{revision}:{path}"])
    except subprocess.CalledProcessError:
        return None


def added_lines(rev_range: str) -> list[tuple[str, int | None, str]]:
    raw = run_git(["diff", "--unified=0", "--no-ext-diff", rev_range])
    lines = raw.decode("utf-8", "replace").splitlines()
    results: list[tuple[str, int | None, str]] = []
    current_file = ""
    new_line: int | None = None

    for line in lines:
        if line.startswith("+++ b/"):
            current_file = normalize_path(line[6:])
            new_line = None
            continue
        if line.startswith("@@"):
            match = re.search(r"\+(\d+)(?:,(\d+))?", line)
            new_line = int(match.group(1)) if match else None
            continue
        if line.startswith("+") and not line.startswith("+++"):
            results.append((current_file, new_line, line[1:]))
            if new_line is not None:
                new_line += 1
        elif not line.startswith("-") and new_line is not None:
            new_line += 1

    return results


def event_payload(path: str | None) -> dict[str, Any]:
    if not path:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError:
        return {}


def labels_from_event(event: dict[str, Any]) -> set[str]:
    pr = event.get("pull_request") or {}
    labels = pr.get("labels") or event.get("labels") or []
    names = set()
    for label in labels:
        if isinstance(label, dict) and label.get("name"):
            names.add(str(label["name"]).strip().lower())
        elif isinstance(label, str):
            names.add(label.strip().lower())
    return names


def body_from_event(event: dict[str, Any]) -> str:
    pr = event.get("pull_request") or {}
    return str(pr.get("body") or "")


def body_pr_type(body: str) -> str | None:
    match = re.search(r"(?im)^\s*pr\s*type\s*:\s*(research|technical)\s*$", body)
    if match:
        return match.group(1).lower()
    return None


def resolve_pr_type(
    event: dict[str, Any],
    explicit_type: str | None,
) -> tuple[str, bool, list[str]]:
    labels = labels_from_event(event)
    body_type = body_pr_type(body_from_event(event))
    errors: list[str] = []

    has_override = bool(labels & OVERRIDE_LABELS)
    if has_override:
        return "override", True, []

    candidates: list[str] = []
    if labels & TECHNICAL_LABELS:
        candidates.append("technical")
    if labels & RESEARCH_LABELS:
        candidates.append("research")
    if body_type:
        candidates.append(body_type)
    if explicit_type:
        candidates.append(explicit_type)

    if "technical" in candidates and "research" in candidates:
        errors.append("Conflicting PR type markers found: research and technical.")
        return "research", False, errors
    if "technical" in candidates:
        return "technical", False, []
    return "research", False, []


def problem_id_for(path: str) -> str | None:
    match = PROBLEM_PATH_RE.match(path)
    return match.group(1) if match else None


def is_research_object(path: str) -> bool:
    return bool(RESEARCH_OBJECT_RE.match(path))


def is_research_support(path: str) -> bool:
    return bool(RESEARCH_SUPPORT_RE.match(path))


def is_technical_allowed(path: str) -> bool:
    if path in TECHNICAL_ALLOWED_ROOT_FILES:
        return True
    return path.startswith(TECHNICAL_ALLOWED_PREFIXES)


def is_blocked_binary_path(path: str) -> bool:
    suffix = PurePosixPath(path).suffix.lower()
    return suffix in BLOCKED_BINARY_EXTENSIONS


def is_binary_content(data: bytes) -> bool:
    return b"\0" in data


def max_size_for(path: str) -> int:
    if path.startswith("catalog/imports/") and path.endswith((".yaml", ".yml")):
        return MAX_CATALOG_IMPORT_BYTES
    return MAX_REGULAR_FILE_BYTES


def has_frontmatter(text: str) -> bool:
    if not text.startswith("---\n"):
        return False
    return "\n---\n" in text[4:]


def frontmatter_block(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end == -1:
        return ""
    return text[4:end]


def frontmatter_value(text: str, key: str) -> str | None:
    frontmatter = frontmatter_block(text)
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*:\s*([^#\s]+)", frontmatter)
    if not match:
        return None
    return match.group(1).strip().strip("\"'")


def validate_research_object(path: str, text: str) -> list[str]:
    errors: list[str] = []
    if not has_frontmatter(text):
        errors.append(f"{path}: research object files must start with YAML frontmatter.")

    for required in ("id:", "status:"):
        if required not in text:
            errors.append(f"{path}: missing `{required}` in frontmatter.")

    frontmatter = frontmatter_block(text)
    if "ai_assistance:" not in frontmatter:
        errors.append(f"{path}: missing `ai_assistance:` in frontmatter.")

    status = frontmatter_value(text, "status")
    if status and status not in ALLOWED_STATUSES:
        errors.append(
            f"{path}: status `{status}` is not allowed; use docs/status-levels.md."
        )

    if "/proposals/" in path or "/refuted/" in path:
        if "type:" not in text:
            errors.append(f"{path}: missing `type:` in frontmatter.")
        if "source_ids:" not in text and "depends_on:" not in text:
            errors.append(f"{path}: missing `source_ids:` or `depends_on:`.")
        if "# Gap" not in text and "# Known Obstructions" not in text:
            errors.append(f"{path}: missing `# Gap` or `# Known Obstructions`.")
        if "# Next Step" not in text:
            errors.append(f"{path}: missing `# Next Step`.")

    if "/review/" in path:
        if "review_target:" not in text:
            errors.append(f"{path}: review files must include `review_target:`.")
        if "# Recommendation" not in text:
            errors.append(f"{path}: review files must include `# Recommendation`.")

    return errors


def validate_global_rules(
    rev_range: str,
    files: list[ChangedFile],
    revision: str,
) -> list[str]:
    errors: list[str] = []

    for item in files:
        path = item.path
        if item.status == "D":
            continue
        if is_blocked_binary_path(path):
            errors.append(f"{path}: binary/blob file type is not allowed in PRs.")
            continue

        data = file_bytes_at(revision, path)
        if data is None:
            continue
        if is_binary_content(data):
            errors.append(f"{path}: binary content is not allowed in PRs.")
        max_size = max_size_for(path)
        if len(data) > max_size:
            errors.append(
                f"{path}: file is {len(data)} bytes, above the {max_size} byte limit."
            )

    for path, line_number, line in added_lines(rev_range):
        location = f"{path}:{line_number}" if line_number else path
        if RAW_TRANSCRIPT_RE.match(line):
            errors.append(f"{location}: raw chat transcript markers are not allowed.")
        if REVIEW_TRUE_RE.match(line):
            errors.append(
                f"{location}: do not add reviewed=true flags in PR content; "
                "review state is assigned by separate review."
            )

    return errors


def validate_research_pr(files: list[ChangedFile], revision: str) -> list[str]:
    errors: list[str] = []
    paths = [item.path for item in files]
    problem_ids = {problem_id_for(path) for path in paths if problem_id_for(path)}
    problem_ids.discard(None)

    if len(problem_ids) > 1:
        errors.append(
            "Research PRs must touch only one problem workspace. "
            f"Found: {', '.join(sorted(problem_ids))}."
        )

    object_paths: list[str] = []
    for item in files:
        path = item.path
        if path.startswith("problems/_template/"):
            errors.append(f"{path}: template changes belong in a technical PR.")
            continue
        if "/canonical/" in path:
            errors.append(f"{path}: research PRs may not edit canonical files.")
            continue
        if is_research_object(path):
            object_paths.append(path)
            continue
        if is_research_support(path):
            continue
        errors.append(
            f"{path}: research PRs may only edit one problem workspace, using "
            "proposal/review/refuted objects plus graph.yaml or references.bib "
            "support files."
        )

    if not object_paths:
        errors.append("Research PRs must add or edit at least one research object.")

    for path in object_paths:
        if path.endswith("tasks.md"):
            continue
        data = file_bytes_at(revision, path)
        if data is None:
            continue
        text = data.decode("utf-8", "replace")
        errors.extend(validate_research_object(path, text))

    return errors


def validate_technical_pr(files: list[ChangedFile]) -> list[str]:
    errors: list[str] = []
    for item in files:
        path = item.path
        if path.startswith("problems/") and not path.startswith("problems/_template/"):
            errors.append(f"{path}: technical PRs may not edit problem workspaces.")
            continue
        if not is_technical_allowed(path):
            errors.append(f"{path}: path is not allowed in a technical PR.")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check LemmaTrail PR shape rules.")
    parser.add_argument(
        "rev_range",
        help="Git revision range to check, for example origin/main...HEAD.",
    )
    parser.add_argument(
        "--event-path",
        default=os.environ.get("GITHUB_EVENT_PATH"),
        help="GitHub event JSON path. Defaults to GITHUB_EVENT_PATH.",
    )
    parser.add_argument(
        "--pr-type",
        choices=("research", "technical"),
        help="Override PR type for local testing.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    event = event_payload(args.event_path)
    pr_type, override, type_errors = resolve_pr_type(event, args.pr_type)

    if type_errors:
        for error in type_errors:
            print(f"PR guard error: {error}", file=sys.stderr)
        return 1

    if override:
        print("PR guard skipped: maintainer override label is present.")
        return 0

    files = changed_files(args.rev_range)
    revision = head_revision(args.rev_range)
    errors = validate_global_rules(args.rev_range, files, revision)

    if pr_type == "technical":
        errors.extend(validate_technical_pr(files))
    else:
        errors.extend(validate_research_pr(files, revision))

    if errors:
        print(f"PR guard failed for {pr_type} PR:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"PR guard passed for {pr_type} PR.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
