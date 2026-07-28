# certified-discovery

The landing page for a toolkit built on one asymmetry: **checking a proof is cheap and auditable, so
the thing that produced it does not have to be trusted.**

**→ [nickharris808.github.io/certified-discovery](https://nickharris808.github.io/certified-discovery/)**

## What is in this repository

| File | What it is |
|---|---|
| `artifacts.json` | The single source: every artifact, its URL, and what it is for. |
| `build.py` | Generates `docs/index.html` from that file. No framework, no bundler, no JavaScript. |
| `check_links.py` | Fetches every advertised URL. Run in CI, and weekly on a schedule. |
| `docs/index.html` | The page GitHub Pages serves. Generated — edit `artifacts.json` and rebuild. |

```bash
python build.py            # regenerate the page
python check_links.py      # fetch every URL it advertises
pytest -q                  # the page is current, consistent, and self-describing
```

## Why the link checker exists

A portfolio page whose links have gone stale is worse than no page: it is a set of confident claims
about things that are not there. So the URLs are data rather than markup, one checker reads that
data, and a test asserts the page advertises no link the checker does not know about. A network
failure is reported as *"could not reach"* and still fails the build — it is a check that did not
run, not evidence the link is dead.

## The rule the artifacts share

Every tool in this portfolio has a third verdict that is neither pass nor fail — `UNVERIFIED`,
`OUT_OF_SCOPE`, `UNDECIDED` — so that "I did not establish this" never has to be rounded to "fine".
A verifier that returns a confident answer it has not earned is worse than no verifier, because it
is believed.

Apache-2.0.
