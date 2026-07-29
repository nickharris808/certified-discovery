# certified-discovery

The landing page for a toolkit built on one asymmetry: **checking a proof is cheap and auditable, so
the thing that produced it does not have to be trusted.**

**→ [nickharris808.github.io/certified-discovery](https://nickharris808.github.io/certified-discovery/)**

## 30-second quickstart

```bash
git clone https://github.com/nickharris808/certified-discovery && cd certified-discovery
python build.py
```
```
wrote docs/index.html (11 KB)
wrote docs/concepts.html (10 KB)
wrote docs/tutorial.html (10 KB)
wrote docs/architecture.html (10 KB)
wrote docs/faq.html (10 KB)
10 artifacts, 5 pages
```

Open `docs/index.html` in a browser — there is no server to run and no toolchain to install. Then:

```bash
python check_links.py --page   # fetches all 12 advertised URLs
pytest -q                      # 16 tests: the pages are current, consistent and self-describing
```

## The artifacts

| | |
|---|---|
| [certkit](https://github.com/nickharris808/certkit) | the certificate format and its checker |
| [certkit-js](https://github.com/nickharris808/certkit-js) | the same checker, written independently in JavaScript |
| [exploit-counter](https://github.com/nickharris808/exploit-counter) | exact over-acceptance counting |
| [crs-mcp](https://github.com/nickharris808/crs-mcp) | proof-gated review for agents |
| [soundnessbench](https://github.com/nickharris808/soundnessbench) | the benchmark, and its [leaderboard](https://huggingface.co/spaces/nickh007/soundnessbench-leaderboard) |
| [pytest-mutation-verified](https://github.com/nickharris808/pytest-mutation-verified) | proving a regression test can fail |
| [certkit-action](https://github.com/nickharris808/certkit-action) | the gate, as one line of workflow |
| [cve-proof-corpus](https://huggingface.co/datasets/nickh007/cve-proof-corpus) | six real CVE classes with verifying certificates |
| [certkit-demo](https://huggingface.co/spaces/nickh007/certkit-demo) | try the checker in a browser |

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

## Licence and citation

Apache-2.0 ([`LICENSE`](LICENSE)). Each artifact carries its own `CITATION.cff`; cite the one you
used rather than this index.
