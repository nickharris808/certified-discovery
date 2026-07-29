#!/usr/bin/env python3
"""Generate the documentation site.

Five pages. The landing page is built from ``artifacts.json`` -- one source for
the cards and for the link checker, so a card cannot advertise a URL that nothing
fetches. The other four are hand-written HTML fragments in ``pages/``, wrapped in
a shared shell here.

    python build.py

No static-site generator, no theme, no JavaScript, no build step beyond this
file. A five-page site does not need a toolchain, and a toolkit whose argument is
"you should be able to read the thing you rely on" should not ship a front door
you cannot read.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts.json"
DOCS = HERE / "docs"
OUT = DOCS / "index.html"

#: Every page of the site. The body of each is a hand-written HTML fragment in
#: ``pages/``; the index's body is generated from ``artifacts.json``. One
#: template, one stylesheet, no framework -- the site is five pages.
PAGES = [
    ("index.html", "Start here", None),
    ("concepts.html", "What it proves", "concepts.html"),
    ("tutorial.html", "Tutorial", "tutorial.html"),
    ("architecture.html", "Architecture", "architecture.html"),
    ("faq.html", "FAQ", "faq.html"),
]

ROLE_ORDER = ["checker", "measurement", "method", "integration", "data", "demo"]
ROLE_LABEL = {
    "checker": "Checkers — the part you are meant to audit",
    "measurement": "Measurement — how wrong, and how would you know",
    "method": "Method — testing the tests",
    "integration": "Integration — where the gate actually runs",
    "data": "Data",
    "demo": "Try it, without installing anything",
}


def load() -> list[dict]:
    return json.loads(ARTIFACTS.read_text(encoding="utf-8"))["artifacts"]


def card(a: dict) -> str:
    return f"""      <article class="card">
        <h3><a href="{escape(a["url"])}">{escape(a["name"])}</a></h3>
        <p class="kind">{escape(a["kind"])}</p>
        <p class="tagline">{escape(a["tagline"])}</p>
        <p>{escape(a["body"])}</p>
      </article>"""


def nav(current: str) -> str:
    items = []
    for filename, label, _ in PAGES:
        if filename == current:
            items.append(f'<span aria-current="page">{label}</span>')
        else:
            items.append(f'<a href="{filename}">{label}</a>')
    return "    <nav>" + " · ".join(items) + "</nav>"


def build() -> str:
    """The landing page. Kept as ``build()`` because the tests and the staleness
    check call it by that name."""
    artifacts = load()
    sections = []
    for role in ROLE_ORDER:
        group = [a for a in artifacts if a["role"] == role]
        if not group:
            continue
        cards = "\n".join(card(a) for a in group)
        sections.append(
            f"    <section>\n      <h2>{escape(ROLE_LABEL[role])}</h2>\n"
            f'      <div class="grid">\n{cards}\n      </div>\n    </section>'
        )
    body = INDEX_BODY.replace("__SECTIONS__", "\n\n".join(sections)).replace(
        "__COUNT__", str(len(artifacts))
    )
    return page(
        "index.html", "Certified discovery — check the proof, not the promise", body
    )


def build_page(filename: str) -> str:
    """Wrap a hand-written fragment from ``pages/`` in the shared template."""
    fragment = (HERE / "pages" / filename).read_text(encoding="utf-8")
    title = _title_of(fragment)
    return page(filename, f"{title} — certified discovery", fragment)


def _title_of(fragment: str) -> str:
    import re as _re

    match = _re.search(r"<h1>(.*?)</h1>", fragment, _re.DOTALL)
    return match.group(1).strip() if match else "certified discovery"


def page(filename: str, title: str, body: str) -> str:
    return (
        TEMPLATE.replace("__TITLE__", title)
        .replace("__NAV__", nav(filename))
        .replace("__BODY__", body)
    )


def build_all() -> dict[str, str]:
    """Every page, by filename. The one function CI and the tests compare against."""
    out = {"index.html": build()}
    for filename, _, source in PAGES:
        if source:
            out[filename] = build_page(source)
    return out


TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>__TITLE__</title>
    <meta
      name="description"
      content="A toolkit built on one asymmetry: checking a proof is cheap and auditable, so the
      thing that produced it does not have to be trusted."
    />
    <style>
      :root { color-scheme: light dark; }
      * { box-sizing: border-box; }
      body {
        margin: 0 auto; max-width: 62rem; padding: 2rem 1.25rem 5rem;
        font: 16px/1.65 system-ui, -apple-system, "Segoe UI", sans-serif;
        color: #17181a; background: #fff;
      }
      nav { margin-bottom: 2.5rem; font-size: .93rem; color: #8b9098; }
      nav a { color: #6a6f76; }
      nav [aria-current] { color: #17181a; font-weight: 600; }
      h1 { font-size: 2.1rem; line-height: 1.2; margin: 0 0 .5rem; letter-spacing: -.02em; }
      h2 { font-size: 1.05rem; text-transform: uppercase; letter-spacing: .08em;
           color: #6a6f76; margin: 3rem 0 1rem; font-weight: 600; }
      h3 { margin: 2rem 0 .15rem; font-size: 1.1rem; }
      p, li { max-width: 46rem; }
      a { color: #0a58ca; text-decoration: none; }
      a:hover { text-decoration: underline; }
      code { background: #f2f3f5; padding: .1rem .3rem; border-radius: 3px; font-size: .9em; }
      pre { background: #f7f8f9; border: 1px solid #e3e5e8; border-radius: 8px; padding: 1rem;
            overflow-x: auto; max-width: 52rem; }
      pre code { background: none; padding: 0; font-size: .86rem; line-height: 1.5; }
      table { border-collapse: collapse; margin: 1rem 0; max-width: 52rem; font-size: .93rem; }
      th, td { border: 1px solid #e3e5e8; padding: .45rem .7rem; text-align: left;
               vertical-align: top; }
      th { background: #f7f8f9; }
      .lede { font-size: 1.15rem; color: #33373d; max-width: 44rem; }
      .rule { max-width: 44rem; border-left: 3px solid #17181a; padding-left: 1rem;
              margin: 2rem 0; }
      .grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr)); }
      .card { border: 1px solid #e3e5e8; border-radius: 10px; padding: 1.1rem 1.2rem; }
      .card h3 { margin-top: 0; }
      .card p { margin: .5rem 0 0; font-size: .93rem; color: #3c4046; }
      .kind { font-size: .78rem !important; text-transform: uppercase; letter-spacing: .06em;
              color: #8b9098 !important; margin-top: 0 !important; }
      .tagline { font-weight: 600; color: #17181a !important; }
      footer { margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid #e3e5e8;
               color: #6a6f76; font-size: .9rem; }
      @media (prefers-color-scheme: dark) {
        body { color: #e9ebee; background: #101214; }
        h3 { color: #e9ebee; }
        nav [aria-current] { color: #e9ebee; }
        .lede { color: #c3c7cc; }
        .rule { border-left-color: #e9ebee; }
        .card { border-color: #262a2e; }
        .card p { color: #b3b8bf; }
        .tagline { color: #e9ebee !important; }
        code { background: #1b1f23; }
        pre { background: #16191c; border-color: #262a2e; }
        th, td { border-color: #262a2e; }
        th { background: #16191c; }
        a { color: #79a9ff; }
        footer { border-top-color: #262a2e; }
      }
    </style>
  </head>
  <body>
__NAV__

__BODY__

    <footer>
      <p>
        Apache-2.0. Sources on <a href="https://github.com/nickharris808">GitHub</a>; datasets and
        demos on <a href="https://huggingface.co/nickh007">Hugging Face</a>.
      </p>
      <p>
        Every link on this site is fetched by CI. Every number in each project's README is
        reproducible by running that project's code.
      </p>
    </footer>
  </body>
</html>
"""

INDEX_BODY = """    <h1>Check the proof, not the promise.</h1>

    <p class="lede">
      __COUNT__ open-source artifacts built on one asymmetry: <strong>checking a proof is cheap and
      auditable, so the thing that produced it does not have to be trusted.</strong> The producer can
      be a solver, a model, or a stranger. The checker fits in an afternoon of reading.
    </p>

    <div class="rule">
      <p style="margin:0">
        The rule every one of these follows: <strong>when in doubt, refuse.</strong> Each tool has a
        third verdict that is neither pass nor fail — <code>UNVERIFIED</code>,
        <code>OUT_OF_SCOPE</code>, <code>UNDECIDED</code> — and it exists so that "I did not
        establish this" never has to be rounded to "fine". A verifier that returns a confident answer
        it has not earned is worse than no verifier, because it is believed.
      </p>
    </div>

    <p>
      New here? <a href="concepts.html">What it proves, and what it does not</a> is the five-minute
      version. <a href="tutorial.html">The tutorial</a> takes one real bounds check end to end.
    </p>

__SECTIONS__
"""


if __name__ == "__main__":
    DOCS.mkdir(parents=True, exist_ok=True)
    for name, html in build_all().items():
        (DOCS / name).write_text(html, encoding="utf-8")
        print(f"wrote {DOCS / name} ({len(html) / 1024:.0f} KB)")
    print(f"{len(load())} artifacts, {len(PAGES)} pages")
