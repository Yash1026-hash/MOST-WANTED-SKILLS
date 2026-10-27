# MOST-WANTED-SKILLS

The only skills I need, every time. One repo, drop into any agent.

## The skills

| Skill | What it does | License |
|---|---|---|
| [`okf`](skills/okf) | Google Open Knowledge Format v0.2 bundles: create, read, validate, maintain, with a stdlib-only validator. | Mine |
| [`skill-creator`](skills/skill-creator) | Create, test and improve skills. | Apache-2.0 (Anthropic) |
| [`mcp-builder`](skills/mcp-builder) | Build well-designed MCP servers. | Apache-2.0 (Anthropic) |
| [`frontend-design`](skills/frontend-design) | Distinctive, non-templated UI design. | Apache-2.0 (Anthropic) |
| [`deep-research`](skills/deep-research) | Multi-source research and comparisons. | Unspecified |
| [`humanize-writing`](skills/humanize-writing) | Strip AI-sounding tells from writing. | Unspecified |
| [`llm-council`](skills/llm-council) | 5-advisor debate for high-stakes decisions. | Unspecified |

`docx`, `pdf`, `pptx` and `xlsx` (Anthropic proprietary) are not included. Use the copies built into Claude.

## Install

```bash
git clone https://github.com/Yash1026-hash/MOST-WANTED-SKILLS.git
cd MOST-WANTED-SKILLS
```

| Tool | Command |
|---|---|
| Claude Code | `mkdir -p ~/.claude/skills && cp -r skills/* ~/.claude/skills/` |
| Google Antigravity | `mkdir -p ~/.gemini/antigravity/skills && cp -r skills/* ~/.gemini/antigravity/skills/` (per-workspace: `.agent/skills/`) |
| Codex / other Agent-Skills tools | `mkdir -p ~/.codex/skills && cp -r skills/* ~/.codex/skills/` |
| Claude.ai | zip one skill folder, upload under Settings → Capabilities → Skills |
| ChatGPT, Cursor, Windsurf, Copilot | paste [`portable/OKF-PORTABLE.md`](portable/OKF-PORTABLE.md) into custom instructions or the rules file |

Skill folder paths vary by tool version; check that tool's docs if one isn't picked up.

## Everything else is waste

See [`REMOVE-THESE-SKILLS.md`](REMOVE-THESE-SKILLS.md) for the skills to disable.

## Adding a skill

`skills/<name>/SKILL.md` with `name` and `description` frontmatter, a row in the table above, and its license noted.
