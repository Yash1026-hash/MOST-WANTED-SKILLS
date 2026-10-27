---
name: humanize-writing
description: Detect and remove "AI-sounding" writing tells (based on Wikipedia's Signs of AI Writing essay) from any text Claude drafts or edits. Use this whenever the user asks Claude to "sound less like AI," "sound more human," "humanize" text, "stop writing like ChatGPT," or asks Claude to check a document/email/post/article for AI writing tells before sending. Also consult this proactively whenever Claude is about to produce prose-heavy output (articles, emails, reports, essays, marketing copy, Wikipedia-style content) longer than a couple paragraphs — self-check the draft against this list before delivering it, even if the user didn't explicitly ask for a humanness check.
---

# Humanize Writing

A checklist-driven skill for catching the specific patterns that make text read as AI-generated, and for rewriting text to remove them. Based on Wikipedia's "Signs of AI Writing" essay (WP:AISIGNS), which catalogued thousands of real AI-generated edits to build an empirical list of tells.

## When to use this

- User explicitly asks to "humanize," "de-AI," or "make this sound less like ChatGPT"
- User asks Claude to review a draft (theirs or Claude's) for AI-writing tells before it goes out
- Claude is about to hand over any medium-or-longer piece of prose (article, blog post, report section, bio, email, Wikipedia-style content) — do a silent self-check against the checklist below before finalizing
- User pastes text and asks "does this sound AI-written?"

## Workflow

1. **Read the full text first.** Don't spot-fix line by line on a first pass — get the overall shape.
2. **Scan against the checklist below.** Mark instances of each category that applies. Don't flag single, isolated occurrences of weak signals (see "Weak signals" section) — those alone don't prove anything.
3. **Prioritize fixes** by strength of signal (see ranking below) and by density — a text with 5+ different categories present reads much more "AI" than one with a single stray em dash.
4. **Rewrite, don't just remove.** Cutting "It's important to note that X" down to "X" is usually right. But cutting a whole significance-inflation sentence may leave a gap — check whether the underlying fact still needs to be there, just stated plainly.
5. **Vary sentence rhythm** after decluttering — AI prose tends toward uniform sentence length; deliberately mix short and long once the tells are gone.
6. **Do a final read aloud (mentally)** — human writing has more irregularity, specificity, and occasional roughness than a scrubbed, symmetrical AI paragraph.

## Strong signals (high confidence, fix these first)

- **Broken/fake citation artifacts**: leftover `citeturn0search0`, `oaicite`, `[cite: 12]`, `contentReference`, `utm_source=chatgpt.com`/`openai`, placeholder dates like `2025-XX-XX`, unfilled brackets like `[INSERT LINK HERE]`
- **Markdown bleeding into the wrong format**: `**bold**`/`#` headers pasted into a context that needs different markup (e.g. wikitext, plain email)
- **Chatbot-voice leakage**: "I hope this helps!", "Would you like me to also...", "Certainly! Here's a draft:", "Let me know if you'd like adjustments"
- **Knowledge-cutoff disclaimers**: "As of my last update...", "specific details are limited in available sources," "not widely documented" (often paired with speculation dressed as fact)
- **Un-filled templates**: "[Describe the specific section here]", "[Your Name]"

## Core content/style signals (the bulk of real-world AI tells)

**Vocabulary clustering** — watch for multiple of these in one passage: *delve, boast(s), tapestry, testament, underscore, pivotal, intricate, meticulous, foster, garner, robust, showcase, landscape (abstract), key, crucial, vibrant, align with, bolstered, enhance, fostering, highlight (verb), interplay, valuable insights*. One word alone means nothing; a cluster is a strong tell.

**Significance inflation** — sentences that assert importance instead of showing it: "stands as a testament to," "marking a pivotal moment," "cementing its legacy," "reflects broader trends," "underscores its significance." Fix: state the fact, cut the interpretive tail, let the reader judge significance.

**Notability-flexing / citation-padding** — listing every outlet that covered a subject, or "maintains an active social media presence." Fix: state the one or two facts that matter; don't enumerate as proof.

**Dangling participle analysis** — sentences ending in an unearned "-ing" clause: "...creating a lively community," "...highlighting its enduring impact." Fix: cut the clause or replace with a concrete fact.

**Vague/weasel attribution** — "experts argue," "researchers note," "industry reports suggest" with no real named source, or inflating 1-2 sources into "many." Fix: name the actual source or drop the attribution.

**The formulaic "Challenges" wrap-up** — "Despite its successes, X faces several challenges..." followed by a vague hopeful future-tense close. A dead giveaway in bios/place descriptions/company write-ups.

**Negative parallelism / false contrast** — "Not just X, but Y." "It's not merely A — it's B." Also the reversed "X rather than Y." Manufactures depth from nothing; usually deletable.

**Rule of three overuse** — grouping everything into triads (three adjectives, three examples, three clauses) as a crutch for sounding thorough.

**Elegant variation** — swapping synonyms purely to avoid repeating a word (same person becomes "the artist," then "the visionary," then "the collaborator" within one paragraph). Fix: it's fine to just repeat the plain noun/name.

**Promotional/travel-brochure tone** on neutral subjects — "boasts stunning views," "rich cultural heritage," "nestled in the heart of." Fix: flatten to neutral, specific description.

**Uniform sentence rhythm** — every sentence roughly the same length and subject-verb-object shape. Fix: vary length and structure deliberately.

**Redundant restating** — summarizing a point that was just made two sentences earlier, as if the reader can't retain it. Fix: cut the restatement.

**Formatting tells** — Title Case headers where sentence case is normal; heavy mechanical bolding of "key terms"; bullet lists with a bolded lead-in phrase whose body sentence just re-states the bold phrase; overuse of em dashes (especially spaced ` — `) where a comma/colon/parenthesis reads more natural.

**Overhedging** — dodging a plain yes/no with soft language ("claims are disputed") when the actual answer is a clear "false" or "true."

## Weak signals — do NOT flag these alone

These correlate with AI writing in aggregate studies but are common in normal human writing too. Flagging any single instance of these is a false-positive risk — only note them if several *other* stronger signals are also present:

- Perfect grammar
- Formal/academic tone
- A single transition word ("Additionally," "However")
- Lack of citations
- Curly quotation marks/apostrophes (many editing tools do this by default)
- Markdown alone (common on Reddit, Discord, GitHub, Slack)

## Applying this to Claude's own output

When Claude is drafting something itself (not just reviewing user text), the most useful move is prevention: avoid reaching for the vocabulary cluster and significance-inflation habits in the first place, keep sentence rhythm irregular, cite specifics instead of vague importance claims, and skip the "Challenges/Future Outlook" formula unless it's genuinely structurally appropriate. Don't mention this self-check to the user — just deliver cleaner prose.

## Deeper reference

For the full catalogued examples (real before/after diffs from Wikipedia edits, per-category breakdowns, model-specific quirks like ChatGPT vs. Grok vs. Gemini phrasing differences, and the historical/deprecated tells like "delve" overuse from 2023), see `references/full-catalog.md`. Load it only if you need exhaustive detail beyond the checklist above — the checklist covers what's needed for almost all rewrite/review tasks.
