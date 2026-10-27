# OKF v0.2 spec summary

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
