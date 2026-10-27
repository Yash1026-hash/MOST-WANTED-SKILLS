---
name: okf
description: Create, read, validate, maintain and convert knowledge into Google's Open Knowledge Format (OKF v0.2) bundles - directories of markdown files with YAML frontmatter that give AI agents portable, trustable context (table schemas, metric definitions, runbooks, playbooks, API notes, LLM-wiki style knowledge bases). Use whenever the user mentions OKF, Open Knowledge Format, a knowledge bundle, "agent-readable wiki", "LLM wiki", knowledge catalog, concept files with frontmatter, trust/provenance/freshness fields (generated, verified, sources, stale_after, status), Attested Computation, or wants to turn docs, notes, a repo, schemas or a Notion/Obsidian/Confluence export into structured agent knowledge - even if they never say "OKF".
---

# OKF - Open Knowledge Format v0.2

OKF = a directory of markdown files, each with YAML frontmatter. No registry, no tooling required. One concept per file. Only `type` is required. Spec: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md

This skill is portable: the instructions below work with no tools. `scripts/okf.py` (Python 3, stdlib only) is an optional accelerator for validate/index/report/scaffold.

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
