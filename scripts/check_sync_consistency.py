#!/usr/bin/env python3
"""Consistency gate for github-sync: README version block vs CHANGELOG top version."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

CHANGELOG_TOP = re.compile(r"^##\s*\[(\d+\.\d+\.\d+)\]\s*-\s*(\d{4}-\d{2}-\d{2})", re.M)
README_BLOCK = re.compile(
    r"<!-- github-sync:begin -->\s*"
    r"\*\*Version:\*\*\s*([^\n]+)\s*"
    r"\*\*Last sync:\*\*\s*([^\n]+)\s*"
    r"<!-- github-sync:end -->",
    re.S,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path.cwd())
    p.add_argument("--expect-version", help="Version that must appear in both files")
    p.add_argument("--expect-date", help="Sync date YYYY-MM-DD (default: today)")
    args = p.parse_args()

    repo: Path = args.repo
    readme = repo / "README.md"
    changelog = repo / "CHANGELOG.md"
    expect_date = args.expect_date or dt.date.today().isoformat()
    errors: list[str] = []

    if not readme.is_file() or readme.stat().st_size == 0:
        errors.append("README.md missing or empty")
    if not changelog.is_file():
        errors.append("CHANGELOG.md missing")

    cl_ver = None
    if changelog.is_file():
        m = CHANGELOG_TOP.search(changelog.read_text(encoding="utf-8"))
        if not m:
            errors.append("CHANGELOG.md has no top `## [X.Y.Z] - date` entry")
        else:
            cl_ver, _cl_date = m.group(1), m.group(2)

    if readme.is_file():
        rm = README_BLOCK.search(readme.read_text(encoding="utf-8"))
        if not rm:
            errors.append("README.md missing github-sync version block")
        else:
            rm_ver = rm.group(1).strip()
            rm_date = rm.group(2).strip()
            if args.expect_version and rm_ver != args.expect_version:
                errors.append(f"README version {rm_ver} != expected {args.expect_version}")
            if args.expect_version and cl_ver and cl_ver != args.expect_version:
                errors.append(f"CHANGELOG version {cl_ver} != expected {args.expect_version}")
            if cl_ver and rm_ver != cl_ver:
                errors.append(f"README version {rm_ver} != CHANGELOG {cl_ver}")
            if rm_date != expect_date:
                errors.append(f"README last sync {rm_date} != expected {expect_date}")

    if errors:
        print("FAIL")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"PASS version={cl_ver} date={expect_date}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
