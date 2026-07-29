#!/usr/bin/env python3
"""Fetch every URL the landing page advertises.

A portfolio page whose links have gone stale is worse than no page: it is a set
of confident claims about things that are not there. So CI fetches every one on
a schedule, and a non-200 fails the build.

    python check_links.py            # the artifact list
    python check_links.py --page     # every href in the built page as well
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMEOUT = 45


def urls(include_page: bool) -> list[str]:
    data = json.loads((HERE / "artifacts.json").read_text(encoding="utf-8"))
    found = [a["url"] for a in data["artifacts"]]
    if include_page:
        html = (HERE / "docs" / "index.html").read_text(encoding="utf-8")
        found += re.findall(r'href="(https?://[^"]+)"', html)
    seen: list[str] = []
    for u in found:
        if u not in seen:
            seen.append(u)
    return seen


def fetch(url: str) -> tuple[int, str]:
    request = urllib.request.Request(
        url, headers={"User-Agent": "certified-discovery-linkcheck"}
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return response.status, ""
    except urllib.error.HTTPError as exc:
        return exc.code, exc.reason
    except (urllib.error.URLError, OSError, ValueError) as exc:
        # A network failure is not evidence the link is dead, and must not be
        # reported as if it were. It is still a failure -- the check did not run.
        return 0, f"could not reach: {exc}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--page", action="store_true", help="also check hrefs in the built page"
    )
    args = parser.parse_args()

    bad = []
    for url in urls(args.page):
        status, detail = fetch(url)
        mark = "ok " if status == 200 else "BAD"
        print(f"{mark} {status:>3}  {url}{'  ' + detail if detail else ''}")
        if status != 200:
            bad.append(url)

    if bad:
        print(f"\n{len(bad)} link(s) did not return 200.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
