"""The landing page.

Nothing here checks that the page is pretty. It checks that it cannot make a
claim the rest of the portfolio does not support: no dead structure, no artifact
advertised that the index does not list, and no number that is not derived from
the data.
"""

from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = json.loads((ROOT / "artifacts.json").read_text(encoding="utf-8"))
PAGE = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")


def _build():
    spec = importlib.util.spec_from_file_location("_build", ROOT / "build.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_the_page_is_current():
    assert PAGE == _build().build(), "docs/index.html is stale -- run build.py"


def test_every_artifact_appears_on_the_page():
    for artifact in INDEX["artifacts"]:
        assert artifact["url"] in PAGE, artifact["name"]
        assert artifact["name"] in PAGE


def test_the_page_advertises_no_link_the_index_does_not_list():
    """The link checker reads the index. A hand-added href would go unchecked."""
    hrefs = set(re.findall(r'href="(https?://[^"]+)"', PAGE))
    known = {a["url"] for a in INDEX["artifacts"]}
    profile_pages = {"https://github.com/nickharris808", "https://huggingface.co/nickh007"}
    assert hrefs <= known | profile_pages, hrefs - known - profile_pages


def test_the_count_in_the_prose_matches_the_index():
    """The one number on the page, and it is derived rather than typed."""
    assert f"{len(INDEX['artifacts'])} open-source artifacts" in PAGE


def test_every_artifact_has_all_its_fields():
    for artifact in INDEX["artifacts"]:
        for field in ("name", "tagline", "body", "url", "kind", "role"):
            assert artifact.get(field), f"{artifact.get('name')} is missing {field}"


def test_urls_point_only_at_the_two_accounts_that_may_be_published_to():
    for artifact in INDEX["artifacts"]:
        assert artifact["url"].startswith(
            ("https://github.com/nickharris808/", "https://huggingface.co/datasets/nickh007/",
             "https://huggingface.co/spaces/nickh007/")
        ), artifact["url"]


def test_the_abstention_rule_is_stated_on_the_page():
    """It is the one thing the whole portfolio has in common; a page that sold
    the tools without it would be selling something else."""
    assert "when in doubt, refuse" in PAGE.lower()
    for verdict in ("UNVERIFIED", "OUT_OF_SCOPE", "UNDECIDED"):
        assert verdict in PAGE


def test_the_page_needs_no_javascript_and_no_network_to_render():
    assert "<script" not in PAGE.lower()
    assert "cdn." not in PAGE
    assert "<link" not in PAGE.lower() or "stylesheet" not in PAGE.lower()


def test_the_link_checker_reads_the_same_index():
    spec = importlib.util.spec_from_file_location("_lc", ROOT / "check_links.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert set(module.urls(include_page=False)) == {a["url"] for a in INDEX["artifacts"]}


def test_a_network_failure_is_not_reported_as_a_dead_link():
    """Status 0 means the check did not run. It still fails, but it must not
    claim the link is broken."""
    spec = importlib.util.spec_from_file_location("_lc", ROOT / "check_links.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    status, detail = module.fetch("http://127.0.0.1:1/definitely-not-listening")
    assert status == 0
    assert "could not reach" in detail
