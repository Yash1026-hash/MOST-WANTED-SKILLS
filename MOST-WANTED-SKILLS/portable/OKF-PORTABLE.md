# OKF (Open Knowledge Format v0.2) - portable instructions

Drop-in for any AI tool. No scripts needed. If you can run Python, `scripts/okf.py` in the full skill adds validate/index/report/new.


# OKF - Open Knowledge Format v0.2

OKF = a directory of markdown files, each with YAML frontmatter. No registry, no tooling required. One concept per file. Only `type` is required. Spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

This skill is portable: the instructions below work with no tools. Validate by hand with the checklist below.

## Pick the task

| User wants | Do |
|---|---|
| Turn source material into a bundle | **Author** (below) |
| Read/answer from a bundle | **Consume** (below) |
| Check a bundle | `python scripts/okf.py validate <bundle>` or manual checklist in `references/spec-summary.md` §Conformance |
| Upgrade a v0.1 bundle | **Migrate** (below) |
| Exact field rules, examples | `references/spec-summary.md`, `references/templates.md` |

## Author

1. **Plan the concepts.** One file = one idea (a table, a metric, a playbook, a decision). Split anything that would need two titles. Group in subdirectories by domain, not by type.
2. **Write each concept** with frontmatter:
   ```yaml
   ---
   type: Metric                      # REQUIRED, free text, descriptive
   title: Monthly Active Users       # recommended
   description: One-sentence summary used by indexes and search snippets.
   resource: https://...             # canonical URI of the underlying asset, if one exists
   tags: [product, growth]
   status: stable                    # draft | stable | deprecated (absent = stable)
   generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
   sources:
     - { id: src1, resource: https://..., title: ... }
   ---
   ```
   Body: markdown, prefer headings/tables/fenced code over prose. Conventional headings: `# Schema`, `# Examples`, `# Computation`.
3. **Link concepts** with normal markdown links, bundle-absolute preferred: `[orders](/tables/orders.md)`. Prose says what the relationship is. Broken links are legal (not-yet-written knowledge).
4. **Attribute claims** with footnotes whose label equals a `sources[].id`: `text.[^src1]` + `[^src1]: Title`.
5. **Generate indexes**: `python scripts/okf.py index <bundle> --write` (or hand-write `index.md`: headings + `* [Title](file.md) - description`). Root index may carry only `okf_version: "0.2"` frontmatter; other indexes have none.
6. **Log changes** in `log.md`: `## YYYY-MM-DD` headings, newest first, `* **Update**: ...` bullets.
7. **Validate** before handing back. Fix errors; report remaining warnings.

### Trust rules (do not break these)

- Every timestamp is ISO 8601 **with explicit UTC offset**: `2026-10-26T09:00:00Z`. Never a bare date.
- Actors: `<producer>/<version>` for agents/tools, `human:<id>` for people, `process:<id>` for automation.
- **You are an agent. Record yourself in `generated.by` (e.g. `claude-code/<model>`, `chatgpt/<model>`, `antigravity/<model>`).**
- **Never write a `human:` actor in `verified` unless that person actually confirmed the content in this conversation and told you their id.** Fabricated human verification is the single worst failure for this format. Leaving `verified` out is correct for unreviewed content; it simply reads as "unverified".
- `verified` means "content confirmed against sources/resource". It is not "I wrote it carefully".
- Set `stale_after` (absolute instant) for volatile facts: prices, owners, schemas under active change, anything with an SLA. Skip it for timeless content.
- Do not invent `sources`, `usage_count`, `author`, or `last_modified`. Include a signal only if you actually observed it.
- Preserve unknown frontmatter keys when editing someone else's concept. Never delete fields you don't understand.

### Attested Computation

Use `type: Attested Computation` when a number must be computed one sanctioned way. Required: `runtime`. Provide the computation in a `# Computation` fenced block or via `computation:` path. Declare `parameters` (name/type/required), `executor` (`resource`, `receipt` fields), `attester` (`resource`, deterministic non-LLM check). Agents only supply parameter *values*; they must not edit the computation. OKF stores the contract, it does not execute anything. See `references/templates.md`.

## Consume

1. Read root `index.md` (and subdirectory indexes) first - progressive disclosure. Open only the concepts you need.
2. Triage from frontmatter **before** reading bodies: `type`, `status`, `stale_after`, trust tier.
   - Trust tier: no `verified` -> unverified; non-`human:` verifiers only -> machine-confirmed; any `human:` -> human-reviewed. Advisory, not access control.
   - `status: deprecated` or `now >= stale_after` -> do not present as current. Say it is deprecated/stale and when.
3. Follow links to build context. Tolerate broken links and unknown types.
4. When answering, say which concepts you relied on and surface their trust tier if it matters to the decision (e.g. a metric going to an exec dashboard should be human-reviewed).
5. If concepts contradict, OKF has no merge semantics: report the conflict, prefer the one with higher trust tier and later `generated.at`, and say you did.
6. For an Attested Computation: do not improvise the query. Bind only the declared parameters, run the sanctioned computation, return the receipt, and never display a value whose attestation fails.

## Migrate v0.1 -> v0.2

- `timestamp: X` -> `generated: { by: <actor>, at: <ISO with offset> }` (v0.2 consumers may still read legacy `timestamp`).
- Body `# Citations` list -> `sources:` entries with `resource` (and `id` if cited inline).
- `title`/`description` are now recommended, not required. `type` is the only required key.
- Bare dates -> full ISO 8601 with offset.

## Converting other material

- Repo/docs/wiki/export: one concept per meaningful unit; keep original URL in `resource` and `sources`; set `generated.by` to yourself; leave `verified` off.
- Database/warehouse schema: one concept per table/dataset with a `# Schema` table; put the asset URI in `resource`.
- Obsidian/Notion notes: keep their prose in the body; map folders to subdirectories; convert wikilinks to markdown links with `.md` targets.
- Never flatten a large source into one file. Many small linked concepts beat one long page.

## Output checklist

- [ ] every non-index/log `.md` has frontmatter with non-empty `type`
- [ ] timestamps ISO 8601 with offset; actors in convention
- [ ] no fabricated `verified`, `sources` signals, or `human:` actors
- [ ] indexes regenerated, `log.md` updated if the bundle keeps one
- [ ] validator run (or checklist walked) and result reported honestly

## If you cannot run scripts (ChatGPT chat, web UIs)

Skip `scripts/okf.py`. Author the files in the reply as separate fenced blocks labelled with their bundle path, and walk the checklist above by hand. Tell the user plainly that nothing was machine-validated.


---

# APPENDIX A - Spec summary


Source of truth: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md (v0.2; Google revised it in place to require ISO 8601 timestamps with explicit UTC offset). If the live spec differs from this file, the live spec wins.

## Structure
```
bundle/
  index.md        optional directory listing (no frontmatter, except root may have okf_version)
  log.md          optional chronological history
  <concept>.md    one concept per file
  <subdir>/...
```
Reserved filenames (never concepts): `index.md`, `log.md`. Concept ID = path minus `.md`. Distribute as a git repo (recommended), tarball/zip, or subdirectory.

## Frontmatter keys
| Key | Status | Meaning |
|---|---|---|
| `type` | REQUIRED, non-empty | Free-text kind (`BigQuery Table`, `Metric`, `Playbook`, `Reference`, `Attested Computation`). Unknown types must be tolerated. |
| `title` | recommended | Display name (consumers may derive from filename) |
| `description` | recommended | One sentence; used in indexes/snippets |
| `resource` | recommended where applicable | URI of the underlying asset; absent for abstract concepts |
| `tags` | optional | List of short strings |
| `sources` | optional | List of `{resource (required), id, title, author, usage_count, last_modified}`; sibling `usage_window: {from, to}` |
| `generated` | optional | `{by: actor (required), at: ISO8601}` - who/what last produced the content |
| `verified` | optional | List of `{by: actor, at: ISO8601}`; a bare mapping = one-element list |
| `status` | optional | `draft` / `stable` (default) / `deprecated` |
| `stale_after` | optional | Absolute instant; stale when `now >= stale_after` |
| `runtime`, `parameters`, `computation`, `executor`, `attester` | Attested Computation only | See §Attested Computation |
| anything else | allowed | Consumers MUST preserve unknown keys and MUST NOT reject them |

Legacy v0.1: `timestamp` (superseded by `generated.at`), body `# Citations` (superseded by `sources`). Consumers may fall back to them.

## Actors
`<producer>/<version>` (agents/tools) · `human:<id>` · `process:<id>`. Trust classification keys off the `human:` prefix, so it must only be used for hand-authored or human-confirmed content.

## Trust tiers (derived, advisory)
unverified (no `verified`) < machine-confirmed (verifiers all non-`human:`) < human-reviewed (any `human:` verifier). Source credibility is *inferred* from signals (`author`, `usage_count`, `last_modified`); OKF stores no credibility score. `usage_count` is a coarse liveness/trend signal, not a precise ranking.

## Links and paths
Standard markdown links. Bundle-absolute (`/tables/orders.md`, recommended) or relative (`./x.md`). Link = untyped directed relationship; meaning comes from prose. Broken links must be tolerated. Path-valued fields (`resource`, `sources[].resource`, `computation`, `executor.resource`, `attester.resource`) accept absolute URL, `/bundle-relative`, or relative path. `references/` subdirectory conventionally mirrors external material/run instructions/code inside the bundle.

## Body
Standard markdown; favor headings, lists, tables, fenced code. Conventional headings: `# Schema`, `# Examples`, `# Computation`. Per-claim attribution: footnote label = `sources[].id`.

## index.md
Progressive disclosure. Sections of `* [Title](url) - description`. No frontmatter except root `okf_version: "0.2"`. Generators may synthesize; consumers may synthesize on the fly.

## log.md
`## YYYY-MM-DD` headings (ISO date), newest first, prose bullets, e.g. `* **Update**: ...` (`Creation`, `Deprecation` also conventional).

## Attested Computation
Standalone concept (`type: Attested Computation`) carrying a sanctioned way to compute a value.
- `runtime` REQUIRED (`bigquery`, `postgres`, `dbt`, `python`, `Looker`...). Defines what `parameters` mean.
- `parameters`: list of `{name, type, required}`.
- `computation`: optional path; absent => the `# Computation` body fence is the computation.
- `executor`: `{resource, receipt: [fields the run must return]}`.
- `attester`: `{resource}` - deterministic, no-LLM code that checks a receipt; runs consumer-side.
- Agent may only supply parameter values; must not author/edit the computation.
- `verified` (definition still matches policy; slow, stored in bundle) is distinct from attestation (this run used the sanctioned computation; per-call, runtime, not stored).
- Consumer flow: discover -> load contract -> parameterize -> execute -> attest -> gate (refuse failing attestation; warn/refuse when stale).

## Conformance (§11)
A bundle is conformant if: (1) every non-reserved `.md` has parseable YAML frontmatter, (2) every frontmatter has non-empty `type`, (3) `index.md`/`log.md` follow their structure when present. Consumers MUST NOT reject for: missing optional fields, unknown types, unknown keys, broken links, missing indexes.

## Versioning
`okf_version: "0.2"` allowed in root `index.md` frontmatter. Minor bump = backward-compatible additions; major = breaking. Unknown version => best-effort consumption.

## Out of scope / deferred in v0.2
Runtime protocol (receipt/verdict wire formats), attester ABI and sandboxing, attestation caching, semantic-layer templates, merge semantics for contradictory concepts, live-vs-static freshness (OKF is file-based; staleness is a process problem).

## Naming caution
Unrelated things share the abbreviation: the Open Knowledge Foundation, and an OKF-SCIS supply-chain spec. This skill is Google's Open Knowledge Format only.

---

# APPENDIX B - Templates


Replace placeholders. Use real timestamps with offset. Omit any field you cannot honestly fill (especially `verified`).

## Table / data asset
```markdown
---
type: BigQuery Table
title: Customer Orders
description: One row per completed customer order across all channels.
resource: https://console.cloud.google.com/bigquery?p=acme&d=sales&t=orders
tags: [sales, orders]
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
---

# Schema

| Column | Type | Description |
|---|---|---|
| `order_id` | STRING | Globally unique order identifier. |
| `customer_id` | STRING | FK into [customers](/tables/customers.md). |

# Examples

    SELECT COUNT(*) FROM sales.orders WHERE placed_at >= '2026-01-01'
```

## Metric
```markdown
---
type: Metric
title: Monthly Active Users
description: Distinct users with at least one qualifying event in a calendar month.
tags: [product]
status: stable
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
stale_after: 2027-01-26T00:00:00Z
---

# Definition
...computed by [the MAU computation](/computations/mau.md).
```

## Playbook (no resource)
```markdown
---
type: Playbook
title: "Incident response: data freshness alert"
description: Steps to triage a freshness alert on the orders pipeline.
tags: [oncall]
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
---

# Trigger
# Steps
1. ...
```

## Reference / decision / glossary term
```markdown
---
type: Reference
title: Fiscal year definition
description: Acme's fiscal year runs Feb 1 - Jan 31.
sources:
  - { id: policy, resource: https://wiki.example/finance/calendar, title: Finance calendar }
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
---
Fiscal year starts 1 February.[^policy]

[^policy]: Finance calendar
```

## Attested Computation
```markdown
---
type: Attested Computation
title: Revenue for fiscal year
description: Recognized revenue for a fiscal year, per Finance's definition.
status: stable
runtime: bigquery
parameters:
  - { name: year, type: integer, required: true }
executor:
  resource: references/skills/run-on-bq.md
  receipt: [job_id, executed_sql, result]
attester:
  resource: references/attesters/sql-equality.py
generated: { by: <producer>/<version>, at: 2026-10-26T09:00:00Z }
verified: { by: human:<id>, at: 2026-10-26T09:00:00Z }   # ONLY if that human confirmed it
stale_after: 2027-01-26T00:00:00Z
sources:
  - { id: rev-policy, resource: https://wiki.example/finance/revenue-recognition, title: Revenue recognition policy }
---

# Computation

    SELECT SUM(amount) AS revenue
    FROM finance.recognized_revenue
    WHERE fiscal_year = @year

Per the recognition policy.[^rev-policy]

[^rev-policy]: Revenue recognition policy
```

## Root index.md
```markdown
---
okf_version: "0.2"
---

# Metrics

* [Monthly Active Users](metrics/mau.md) - Distinct users with a qualifying event in a month.

# Subdirectories

* [tables](tables/)
```

## log.md
```markdown
# Directory Update Log

## 2026-10-26
* **Creation**: Added [Customer Orders](/tables/orders.md).
```
