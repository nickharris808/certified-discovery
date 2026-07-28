#!/usr/bin/env python3
"""Generate the landing page from ``artifacts.json``.

One source for the page and for the link checker, so a card cannot advertise a
URL that nothing fetches. Regenerate with::

    python build.py

and ``docs/index.html`` updates. The page has no build tooling, no CSS
framework, and no JavaScript: it is a single file of hand-written HTML, which is
about as much machinery as ten links deserve.
"""

from __future__ import annotations

import json
from html import escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts.json"
OUT = HERE / "docs" / "index.html"

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


def build() -> str:
    artifacts = load()
    sections = []
    for role in ROLE_ORDER:
        group = [a for a in artifacts if a["role"] == role]
        if not group:
            continue
        cards = "\n".join(card(a) for a in group)
        sections.append(
            f'    <section>\n      <h2>{escape(ROLE_LABEL[role])}</h2>\n'
            f'      <div class="grid">\n{cards}\n      </div>\n    </section>'
        )
    return TEMPLATE.replace("__SECTIONS__", "\n\n".join(sections)).replace(
        "__COUNT__", str(len(artifacts))
    )


TEMPLATE = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Certified discovery — check the proof, not the promise</title>
    <meta
      name="description"
      content="A toolkit built on one asymmetry: checking a proof is cheap and auditable, so the
      thing that produced it does not have to be trusted."
    />
    <style>
      :root { color-scheme: light dark; }
      * { box-sizing: border-box; }
      body {
        margin: 0 auto; max-width: 62rem; padding: 3rem 1.25rem 5rem;
        font: 16px/1.65 system-ui, -apple-system, "Segoe UI", sans-serif;
        color: #17181a; background: #fff;
      }
      h1 { font-size: 2.1rem; line-height: 1.2; margin: 0 0 .5rem; letter-spacing: -.02em; }
      h2 { font-size: 1.05rem; text-transform: uppercase; letter-spacing: .08em;
           color: #6a6f76; margin: 3rem 0 1rem; font-weight: 600; }
      h3 { margin: 0 0 .15rem; font-size: 1.1rem; }
      a { color: #0a58ca; text-decoration: none; }
      a:hover { text-decoration: underline; }
      .lede { font-size: 1.15rem; color: #33373d; max-width: 44rem; }
      .rule { max-width: 44rem; border-left: 3px solid #17181a; padding-left: 1rem;
              margin: 2rem 0; }
      .grid { display: grid; gap: 1rem; grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr)); }
      .card { border: 1px solid #e3e5e8; border-radius: 10px; padding: 1.1rem 1.2rem; }
      .card p { margin: .5rem 0 0; font-size: .93rem; color: #3c4046; }
      .kind { font-size: .78rem !important; text-transform: uppercase; letter-spacing: .06em;
              color: #8b9098 !important; margin-top: 0 !important; }
      .tagline { font-weight: 600; color: #17181a !important; }
      footer { margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid #e3e5e8;
               color: #6a6f76; font-size: .9rem; }
      @media (prefers-color-scheme: dark) {
        body { color: #e9ebee; background: #101214; }
        h3 { color: #e9ebee; }
        .lede { color: #c3c7cc; }
        .rule { border-left-color: #e9ebee; }
        .card { border-color: #262a2e; }
        .card p { color: #b3b8bf; }
        .tagline { color: #e9ebee !important; }
        a { color: #79a9ff; }
        footer { border-top-color: #262a2e; }
      }
    </style>
  </head>
  <body>
    <h1>Check the proof, not the promise.</h1>

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

__SECTIONS__

    <footer>
      <p>
        Apache-2.0. Sources on <a href="https://github.com/nickharris808">GitHub</a>; datasets and
        demos on <a href="https://huggingface.co/nickh007">Hugging Face</a>.
      </p>
      <p>
        Every link on this page is fetched by CI. Every number in each project's README is
        reproducible by running that project's code.
      </p>
    </footer>
  </body>
</html>
"""


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB, {len(load())} artifacts)")
