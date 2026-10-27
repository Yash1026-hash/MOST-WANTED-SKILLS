# Full Catalog: Signs of AI Writing

Extended reference, paraphrased and organized from Wikipedia's WP:AISIGNS essay (a crowd-sourced catalog of real AI-generated edits caught by Wikipedia editors). Load this only when the top-level SKILL.md checklist isn't detailed enough for the task at hand.

## Why these patterns exist

LLMs generate the statistically most likely continuation given their training data. This causes a "regression to the mean": specific, unusual, textured facts get smoothed into generic, positive-sounding statements. A person's specific achievement ("invented the first train-coupling device") tends to drift toward vague grandeur ("a revolutionary titan of industry"). The subject becomes simultaneously less specific and more hyped — that combination is the real tell, more than any single word choice.

## Content-level patterns (beyond the core checklist)

**Undue emphasis on legacy/significance/broader trends** — LLMs like to connect even mundane facts (population figures, etymology, road networks) to some larger narrative arc. Sometimes paired with a hedge acknowledging the subject is minor, followed by talking about its importance anyway.

**Biology/ecosystem inflation** — when describing a species, LLMs tend to bolt on ecosystem/conservation commentary even when no real conservation status or research exists, e.g. inventing concern about "overfishing, pollution, and habitat destruction" for a fish with no IUCN assessment.

**Outline-like "Future Prospects" sections** — a rigid Challenges → Future Outlook structure appears even in short pieces, ending on a vaguely optimistic note regardless of whether the sources support optimism.

**Leads that treat a generic title as a proper noun** — for article titles that are really just descriptive phrases (e.g. "List of songs about Mexico"), AI-generated ledes often open by defining the phrase as though it were a formal standalone entity: "'List of songs about Mexico' is a curated compilation of..."

## Language/grammar-level patterns

**Avoidance of plain "is/are"** — LLMs prefer "serves as," "stands as," "represents," "boasts," "features," "offers" over the plain copula. "The gallery is X's exhibition arm" becomes "The gallery serves as X's exhibition space." This is measurable: is/are usage dropped over 10% in academic writing coinciding with GPT-3.5's rise.

**"Refers to" ledes** — instead of "X is a Y," AI-written definitional sentences sometimes hedge into "X refers to..." as though writing a dictionary entry about the term rather than the thing itself.

**Model-era vocabulary drift** — the specific overused words change generation to generation:
- 2023–mid 2024 (GPT-4 era): delve, boasts, bolstered, crucial, emphasizing, enduring, garner, intricate/intricacies, interplay, key, landscape, meticulous, pivotal, underscore, tapestry, testament, valuable, vibrant
- Mid 2024–mid 2025 (GPT-4o era): align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant
- Mid 2025 onward (GPT-5 era): emphasizing, enhance, highlighting, showcasing, plus notability/attribution-flexing phrases (see below)
- Grok specifically: leans on pseudo-scientific words like causal, empirical, correlate; still overuses "underscore"

## Model-specific quirks (useful if you know or suspect which tool produced text)

- **ChatGPT**: heaviest historical em-dash use (OpenAI has since tuned GPT-5.1 to suppress this); leftover `citeturn0search0`/`oaicite`/`contentReference` citation artifacts from copy-pasted chat output; `utm_source=chatgpt.com` appended to links; curly quotes/apostrophes common
- **Grok**: `grok_render_citation_card_json` or `<grok-card>` tags left in pasted text; `referrer=grok.com` on links; "X rather than Y" construction more common than "not X, but Y"
- **Gemini**: `[cite: 1]`-style bracket citations; generally more concise than ChatGPT/Grok; less prone to em-dash overuse
- **Claude**: rarely uses curly quotes; more concise than ChatGPT/Grok; less prone to the "broader context" significance-inflation habit
- **DeepSeek and derivatives**: lenticular-bracket citation markup like `【85†L261-269】`
- **Perplexity**: `[attached_file:1]` / `[web:1]` style tags

## Markup-level patterns

**Wikitext/Markdown confusion**: `##` instead of `==` for headers, `**bold**` instead of `'''bold'''`, parenthetical links instead of bracketed wikilinks, stray triple-backtick fenced code blocks labeled ` ```wikitext `. This specific combination (broken wikitext syntax + intact Markdown syntax) is one of the highest-confidence tells for Wikipedia-specific detection, though it obviously doesn't generalize to non-wiki contexts.

**Skipped heading levels** — jumping straight to `===` (level 3) without ever using `==` (level 2), because chat interfaces render `#`/`##`/`###` and the model doesn't track wiki-specific heading hierarchy.

**Hallucinated templates/categories/infoboxes** — plausible-sounding but nonexistent category or template names (red links), often for concepts that sound like they should exist.

## Citation-level patterns

- Broken external links that were seemingly never real (not found even in web archives)
- Invalid ISBN checksums or unresolvable DOIs
- DOIs that resolve to a completely unrelated paper
- Book citations with no page number and no URL — can't actually be checked against the claim
- Named references defined in a reference list but never actually cited inline in the body (cite errors)
- Reference reuse syntax attempted and botched

## Comment/talk-page-specific patterns

(Relevant mainly for detecting AI-written discussion posts, forum comments, appeals, etc., not article prose)

- Misquoting or inventing policy shortcuts that don't lead anywhere real
- Reflexively reassuring the reader that the writer's own contributions "align with" the relevant guidelines
- Asking the other party to point out specifically what's wrong, rather than substantively engaging
- Accusing critics of judging based on "style alone" without stronger evidence
- Overly exhaustive, first-person, policy-quoting explanations for very small edits

## Meta-level / weak circumstantial signals

Useful only in combination with several stronger signals above, and only for detecting whether *someone else's* text was AI-written (not useful for self-editing):

- A sudden, complete shift in an editor/writer's fluency or grammar relative to their established style
- A mismatch between a writer's likely home dialect/location and the variety of English used (e.g. suddenly all-American spelling from a writer who otherwise uses British spelling)
- Text predating November 30, 2022 (ChatGPT's public launch) can be confidently ruled out as AI-generated

## Explicitly NOT reliable on their own

Do not treat any single instance of these as evidence:
- Perfect grammar
- Mixed casual/formal register
- "Bland" or generic-sounding prose (this is subjective and not specific enough)
- Fancy/academic vocabulary in general (only the *specific* clustered words above are the tell)
- Letter-like formal salutations (long predate LLMs)
- A lone transition word
- Unsourced content (570,000+ genuinely human Wikipedia articles lack citations)
- Markdown formatting by itself (ubiquitous on GitHub, Slack, Reddit, Discord, Obsidian)
- Bizarre/garbled wikitext syntax — more often a sign of a broken browser extension or visual editor bug than AI

## Older/historical tells (useful for auditing old text, less useful for catching current AI output)

- Didactic disclaimers: "it's important to note/remember/consider" — common in 2023-era GPT-4 output, now rarer
- Explicit "In summary" / "In conclusion" section wrap-ups
- Outright prompt refusals leaking into text: "As an AI language model, I cannot..."
- Abrupt content cutoffs mid-sentence (token limits)
- Old/mismatched `access-date` values in citations relative to when the edit was actually made
