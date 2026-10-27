# Installing the `okf` skill everywhere

The skill is a standard Agent Skills folder: `okf/SKILL.md` + `scripts/` + `references/`. Tools that read that format can use the folder as is. Everything else gets the single-file version (`OKF-PORTABLE.md`).

Skill folder locations below are the commonly documented ones; tools change them, so if a path doesn't pick the skill up, check that tool's current skills docs.

## Claude Code
```bash
# all projects
mkdir -p ~/.claude/skills && cp -r okf ~/.claude/skills/
# one project
mkdir -p .claude/skills && cp -r okf .claude/skills/
```
Then: "validate my OKF bundle in ./kb" or "turn docs/ into an OKF bundle".

## Google Antigravity
```bash
# one workspace
mkdir -p .agent/skills && cp -r okf .agent/skills/
# global
mkdir -p ~/.gemini/antigravity/skills && cp -r okf ~/.gemini/antigravity/skills/
```

## OpenAI Codex CLI / other Agent-Skills-compatible agents
```bash
mkdir -p ~/.codex/skills && cp -r okf ~/.codex/skills/      # or .agents/skills in a repo
```

## Claude.ai / Claude Desktop
Zip the `okf/` folder (already provided as `okf.zip`) and upload under Settings -> Capabilities -> Skills.

## ChatGPT (no skill folders in chat)
Use `OKF-PORTABLE.md`:
- **Custom GPT / Project:** paste it into Instructions (or upload as a knowledge file and put one line in Instructions: "Follow OKF-PORTABLE.md for any OKF / knowledge-bundle task").
- **One-off chat:** paste it as the first message.
ChatGPT can't run `okf.py` unless Code Interpreter/Python is on; with it on, upload `scripts/okf.py` and tell it to run `python okf.py validate <dir>` on your uploaded bundle (zip it first). Without it, the skill falls back to a manual checklist and says nothing was machine-validated.

## Cursor / Windsurf / Copilot / Aider / anything with a rules file
Append `OKF-PORTABLE.md` to the tool's rules file: `AGENTS.md`, `.cursor/rules/okf.mdc`, `.windsurfrules`, `.github/copilot-instructions.md`, or `CONVENTIONS.md`. For an always-on-but-light option, add only this and keep the skill folder in the repo:
```markdown
## OKF
For any Open Knowledge Format / knowledge-bundle task, read `.okf/SKILL.md` first and follow it.
Never write a `human:` actor in `verified` unless that person confirmed the content.
```

## Verify it works
```bash
python okf/scripts/okf.py new kb tables/orders --type "BigQuery Table" --title Orders --by claude-code/test
python okf/scripts/okf.py index kb --write
python okf/scripts/okf.py validate kb
python okf/scripts/okf.py report kb
```
Expected: `CONFORMANT (OKF v0.2 §11)`.

## Update when the spec changes
Google has already revised v0.2 in place once (timestamps). Re-read SPEC.md occasionally and update `references/spec-summary.md` and the timestamp/field checks in `scripts/okf.py`.
