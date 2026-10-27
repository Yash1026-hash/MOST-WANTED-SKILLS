#!/usr/bin/env python3
"""okf.py - validate / index / report / scaffold OKF v0.2 bundles.

Zero dependencies (stdlib only). Uses PyYAML if installed, otherwise a built-in
YAML-subset parser that covers everything OKF frontmatter uses.

Usage:
  python okf.py validate <bundle> [--strict] [--json]
  python okf.py index    <bundle> [--write]
  python okf.py report   <bundle>
  python okf.py new      <bundle> <concept/path> --type T [--title X] [--desc X] [--by ACTOR] [--tags a,b]
Exit code: 1 if validate finds errors (or warnings with --strict), else 0.
"""
import argparse, json, os, re, sys
from datetime import datetime, timezone

RESERVED = {"index.md", "log.md"}
ISO_TZ = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACTOR = re.compile(r"^(human:.+|process:.+|[^:\s/]+/[^\s]+)$")
STATUSES = {"draft", "stable", "deprecated"}
TS_KEYS = {"at", "last_modified", "stale_after", "from", "to"}

# ---------------------------------------------------------------- YAML subset
def _strip_comment(line):
    out, q = [], None
    for i, ch in enumerate(line):
        if q:
            if ch == q: q = None
        elif ch in "\"'" and (i == 0 or line[i-1] in " [{,:"):
            q = ch
        elif ch == "#" and (i == 0 or line[i-1] == " "):
            break
        out.append(ch)
    return "".join(out).rstrip()

def _scalar(s):
    s = s.strip()
    if s == "" or s in ("~", "null", "Null", "NULL"): return None
    if s[0] in "\"'" and s[-1] == s[0] and len(s) >= 2: return s[1:-1]
    if s[0] == "[" or s[0] == "{": return _flow(s)
    if s in ("true", "True"): return True
    if s in ("false", "False"): return False
    if re.fullmatch(r"-?\d+", s): return int(s)
    if re.fullmatch(r"-?\d+\.\d+", s): return float(s)
    return s

def _split_top(s, sep=","):
    parts, depth, q, cur = [], 0, None, []
    for ch in s:
        if q:
            cur.append(ch)
            if ch == q: q = None
            continue
        if ch in "\"'": q = ch
        elif ch in "[{": depth += 1
        elif ch in "]}": depth -= 1
        if ch == sep and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(ch)
    if "".join(cur).strip(): parts.append("".join(cur))
    return parts

def _kv(text):
    """Split 'key: value' at first ': ' (or trailing ':') outside quotes."""
    q = None
    for i, ch in enumerate(text):
        if q:
            if ch == q: q = None
        elif ch in "\"'" and i == 0: q = ch
        elif ch == ":" and (i + 1 == len(text) or text[i+1] == " "):
            k = text[:i].strip()
            if len(k) >= 2 and k[0] in "\"'" and k[-1] == k[0]: k = k[1:-1]
            return k, text[i+1:].strip()
    return None, text

def _flow(s):
    s = s.strip()
    if s.startswith("["):
        return [_scalar(p) for p in _split_top(s[1:-1])]
    if s.startswith("{"):
        d = {}
        for p in _split_top(s[1:-1]):
            k, v = _kv(p.strip())
            if k is not None: d[k] = _scalar(v)
        return d
    return _scalar(s)

def _looks_kv(item):
    if not item or item[0] in "\"'[{": return False
    k, _ = _kv(item)
    return k is not None

def _parse_node(lines, i, indent):
    if lines[i][1].startswith("-"): return _parse_list(lines, i, indent)
    return _parse_map(lines, i, indent)

def _parse_map(lines, i, indent):
    d = {}
    while i < len(lines) and lines[i][0] == indent and not lines[i][1].startswith("- "):
        k, rest = _kv(lines[i][1])
        if k is None: raise ValueError(f"cannot parse line: {lines[i][1]!r}")
        i += 1
        if rest == "":
            if i < len(lines) and (lines[i][0] > indent or (lines[i][0] == indent and lines[i][1].startswith("- "))):
                d[k], i = _parse_node(lines, i, lines[i][0])
            else:
                d[k] = None
        elif rest in ("|", ">", "|-", ">-"):
            buf = []
            while i < len(lines) and lines[i][0] > indent:
                buf.append(lines[i][1]); i += 1
            d[k] = (" " if rest.startswith(">") else "\n").join(buf)
        else:
            d[k] = _scalar(rest)
    return d, i

def _parse_list(lines, i, indent):
    out = []
    while i < len(lines) and lines[i][0] == indent and (lines[i][1].startswith("- ") or lines[i][1] == "-"):
        item = lines[i][1][1:].strip()
        if item == "":
            i += 1
            if i < len(lines) and lines[i][0] > indent:
                v, i = _parse_node(lines, i, lines[i][0]); out.append(v)
            else: out.append(None)
        elif _looks_kv(item):
            lines[i] = (indent + 2, item)
            v, i = _parse_map(lines, i, indent + 2); out.append(v)
        else:
            out.append(_scalar(item)); i += 1
    return out, i

def parse_yaml(text):
    if not os.environ.get("OKF_NO_PYYAML"):
        try:
            import yaml  # type: ignore
            class _Loader(yaml.SafeLoader): pass
            # keep timestamps as strings so offsets are validated, not silently coerced
            _Loader.yaml_implicit_resolvers = {
                k: [(t, r) for t, r in v if t != "tag:yaml.org,2002:timestamp"]
                for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}
            v = yaml.load(text, Loader=_Loader)
            return v if v is not None else {}
        except ImportError:
            pass
    lines = []
    for raw in text.splitlines():
        s = _strip_comment(raw.replace("\t", "  "))
        if s.strip(): lines.append((len(s) - len(s.lstrip(" ")), s.strip()))
    if not lines: return {}
    v, _ = _parse_node(lines, 0, lines[0][0])
    return v

# ------------------------------------------------------------------ documents
def split_frontmatter(text):
    """Return (frontmatter_text|None, body)."""
    if text.startswith("\ufeff"): text = text[1:]
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(\r?\n|$)", text, re.S)
    if not m: return None, text
    return m.group(1), text[m.end():]

def walk(bundle):
    for root, dirs, files in os.walk(bundle):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for f in sorted(files):
            if f.endswith(".md"):
                yield os.path.join(root, f)

def rel(bundle, path): return os.path.relpath(path, bundle).replace(os.sep, "/")

def load_concepts(bundle):
    docs = {}
    for p in walk(bundle):
        name = os.path.basename(p)
        if name in RESERVED: continue
        with open(p, encoding="utf-8") as fh: text = fh.read()
        fm_text, body = split_frontmatter(text)
        fm, err = None, None
        if fm_text is None: err = "no frontmatter block"
        else:
            try:
                fm = parse_yaml(fm_text)
                if not isinstance(fm, dict): err = "frontmatter is not a mapping"; fm = None
            except Exception as e:
                err = f"unparseable frontmatter: {e}"
        docs[rel(bundle, p)] = {"fm": fm, "body": body, "err": err, "path": p}
    return docs

def parse_ts(s):
    if not isinstance(s, str) or not ISO_TZ.match(s): return None
    try: return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError: return None

def as_list(v):
    if v is None: return []
    return v if isinstance(v, list) else [v]

def trust_tier(fm):
    ver = [v for v in as_list(fm.get("verified")) if isinstance(v, dict)]
    if not ver: return "unverified"
    if any(str(v.get("by", "")).startswith("human:") for v in ver): return "human-reviewed"
    return "machine-confirmed"

def is_stale(fm, now=None):
    now = now or datetime.now(timezone.utc)
    t = parse_ts(fm.get("stale_after"))
    return bool(t and now >= t)

# ----------------------------------------------------------------- validation
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

def strip_code(body):
    return re.sub(r"```.*?```|~~~.*?~~~", "", body, flags=re.S)

def check_ts_fields(fm, add, where):
    def chk(key, val):
        if isinstance(val, str) and not ISO_TZ.match(val):
            hint = " (bare date; needs time + UTC offset)" if ISO_DATE.match(val) else ""
            add("warn", where, f"`{key}` is not ISO 8601 with explicit UTC offset: {val!r}{hint}")
        elif val is not None and not isinstance(val, str):
            add("warn", where, f"`{key}` should be a quoted-safe ISO 8601 string, got {type(val).__name__}")
    g = fm.get("generated")
    if isinstance(g, dict) and "at" in g: chk("generated.at", g["at"])
    for v in as_list(fm.get("verified")):
        if isinstance(v, dict) and "at" in v: chk("verified.at", v["at"])
    if "stale_after" in fm: chk("stale_after", fm["stale_after"])
    for s in as_list(fm.get("sources")):
        if isinstance(s, dict):
            if "last_modified" in s: chk("sources[].last_modified", s["last_modified"])
            uw = s.get("usage_window")
            if isinstance(uw, dict):
                for k in ("from", "to"):
                    if k in uw: chk(f"sources[].usage_window.{k}", uw[k])
    uw = fm.get("usage_window")
    if isinstance(uw, dict):
        for k in ("from", "to"):
            if k in uw: chk(f"usage_window.{k}", uw[k])

def validate(bundle):
    issues = []
    def add(level, where, msg): issues.append({"level": level, "file": where, "msg": msg})
    if not os.path.isdir(bundle):
        add("error", bundle, "bundle directory not found"); return issues, {}
    docs = load_concepts(bundle)
    all_ids = set(docs)
    for rid, d in docs.items():
        fm, body = d["fm"], d["body"]
        if d["err"]:
            add("error", rid, d["err"]); continue
        t = fm.get("type")
        if not isinstance(t, str) or not t.strip():
            add("error", rid, "missing or empty required `type`")
        for k in ("title", "description"):
            if not fm.get(k): add("warn", rid, f"recommended `{k}` is missing")
        if "timestamp" in fm and "generated" not in fm:
            add("warn", rid, "legacy v0.1 `timestamp`; v0.2 uses `generated: {by, at}`")
        if re.search(r"^#\s+Citations\b", body, re.M) and "sources" not in fm:
            add("warn", rid, "legacy v0.1 `# Citations`; v0.2 uses `sources` in frontmatter")
        st = fm.get("status")
        if st is not None and st not in STATUSES:
            add("warn", rid, f"`status` should be one of draft|stable|deprecated, got {st!r}")
        g = fm.get("generated")
        if g is not None:
            if not isinstance(g, dict) or not g.get("by"):
                add("warn", rid, "`generated` needs a `by` actor")
            elif not ACTOR.match(str(g["by"])):
                add("warn", rid, f"`generated.by` not in actor form <producer>/<version>, human:<id>, process:<id>: {g['by']!r}")
        for v in as_list(fm.get("verified")):
            if not isinstance(v, dict) or not v.get("by") or not v.get("at"):
                add("warn", rid, "each `verified` entry needs `by` and `at`")
            elif not ACTOR.match(str(v["by"])):
                add("warn", rid, f"`verified.by` not in actor form: {v['by']!r}")
        for s in as_list(fm.get("sources")):
            if not isinstance(s, dict) or not s.get("resource"):
                add("warn", rid, "each `sources` entry needs a `resource`")
        ids = {s.get("id") for s in as_list(fm.get("sources")) if isinstance(s, dict) and s.get("id")}
        for lab in re.findall(r"\[\^([^\]]+)\]", body):
            if ids and lab not in ids and not re.search(rf"^\[\^{re.escape(lab)}\]:", body, re.M):
                add("warn", rid, f"footnote [^{lab}] has no matching `sources[].id`")
        check_ts_fields(fm, lambda l, w, m: add(l, rid, m), rid)
        if is_stale(fm): add("warn", rid, f"stale: `stale_after` {fm.get('stale_after')} has passed")
        if t == "Attested Computation":
            if not fm.get("runtime"): add("error", rid, "Attested Computation requires `runtime`")
            has_fence = bool(re.search(r"^#\s+Computation\b", body, re.M))
            if not has_fence and not fm.get("computation"):
                add("warn", rid, "Attested Computation needs a `# Computation` body fence or a `computation` path")
            if not fm.get("attester"): add("warn", rid, "no `attester` declared; value cannot be attested")
        # links
        for target in LINK.findall(strip_code(body)):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"): continue
            t0 = target.split("#")[0]
            if not t0.endswith(".md"): continue
            tp = t0.lstrip("/") if t0.startswith("/") else os.path.normpath(os.path.join(os.path.dirname(rid), t0)).replace(os.sep, "/")
            if not os.path.exists(os.path.join(bundle, tp)):
                add("info", rid, f"broken link (allowed by spec): {target}")
    # reserved files
    for p in walk(bundle):
        name = os.path.basename(p); rid = rel(bundle, p)
        if name not in RESERVED: continue
        with open(p, encoding="utf-8") as fh: text = fh.read()
        fm_text, body = split_frontmatter(text)
        if name == "index.md":
            if fm_text is not None:
                if os.path.dirname(rid) != "":
                    add("error", rid, "non-root index.md must not have frontmatter")
                else:
                    try:
                        fm = parse_yaml(fm_text) or {}
                        extra = set(fm) - {"okf_version"}
                        if extra: add("error", rid, f"root index.md frontmatter may only contain okf_version, found {sorted(extra)}")
                    except Exception as e:
                        add("error", rid, f"unparseable frontmatter: {e}")
        else:
            for h in re.findall(r"^##\s+(.+?)\s*$", body, re.M):
                if not ISO_DATE.match(h): add("warn", rid, f"log date heading not YYYY-MM-DD: {h!r}")
    return issues, docs

# --------------------------------------------------------------------- index
def build_index(bundle, d, is_root):
    entries, subdirs = {}, []
    for name in sorted(os.listdir(d)):
        full = os.path.join(d, name)
        if name.startswith("."): continue
        if os.path.isdir(full):
            if any(f.endswith(".md") for _, _, fs in os.walk(full) for f in fs): subdirs.append(name)
        elif name.endswith(".md") and name not in RESERVED:
            with open(full, encoding="utf-8") as fh: text = fh.read()
            fm_text, _ = split_frontmatter(text)
            fm = {}
            if fm_text:
                try: fm = parse_yaml(fm_text) or {}
                except Exception: pass
            typ = str(fm.get("type", "Concept"))
            title = fm.get("title") or os.path.splitext(name)[0].replace("-", " ").replace("_", " ")
            entries.setdefault(typ, []).append((title, name, fm.get("description") or ""))
    out = ['---\nokf_version: "0.2"\n---\n'] if is_root else []
    for typ in sorted(entries):
        out.append(f"# {typ}\n")
        for title, name, desc in sorted(entries[typ], key=lambda e: str(e[0]).lower()):
            out.append(f"* [{title}]({name})" + (f" - {desc}" if desc else ""))
        out.append("")
    if subdirs:
        out.append("# Subdirectories\n")
        for s in subdirs: out.append(f"* [{s}]({s}/)")
        out.append("")
    return "\n".join(out).rstrip() + "\n"

# ----------------------------------------------------------------------- cli
def cmd_validate(a):
    issues, _ = validate(a.bundle)
    errs = [i for i in issues if i["level"] == "error"]
    warns = [i for i in issues if i["level"] == "warn"]
    if a.json:
        print(json.dumps(issues, indent=2))
    else:
        for i in issues: print(f"{i['level'].upper():5} {i['file']}: {i['msg']}")
        ok = "CONFORMANT (OKF v0.2 §11)" if not errs else "NOT CONFORMANT"
        print(f"\n{ok}: {len(errs)} error(s), {len(warns)} warning(s), {len(issues)-len(errs)-len(warns)} info")
    return 1 if errs or (a.strict and warns) else 0

def cmd_index(a):
    n = 0
    for root, dirs, files in os.walk(a.bundle):
        dirs[:] = sorted(x for x in dirs if not x.startswith("."))
        if not any(f.endswith(".md") for _, _, fs in os.walk(root) for f in fs): continue
        text = build_index(a.bundle, root, os.path.abspath(root) == os.path.abspath(a.bundle))
        target = os.path.join(root, "index.md")
        if a.write:
            with open(target, "w", encoding="utf-8") as fh: fh.write(text)
            n += 1; print(f"wrote {rel(a.bundle, target)}")
        else:
            print(f"===== {rel(a.bundle, target)} =====\n{text}")
    if a.write: print(f"{n} index file(s) written")
    return 0

def cmd_report(a):
    _, docs = validate(a.bundle)
    rows = []
    for rid, d in sorted(docs.items()):
        fm = d["fm"]
        if not fm: rows.append((rid, "INVALID", "-", "-", "-")); continue
        g = fm.get("generated"); gat = g.get("at", "-") if isinstance(g, dict) else fm.get("timestamp", "-")
        rows.append((rid, str(fm.get("type", "?")), trust_tier(fm),
                     "STALE" if is_stale(fm) else str(fm.get("status", "stable")), str(gat)))
    w = [max(len(str(r[i])) for r in rows + [("concept", "type", "trust", "state", "generated")]) for i in range(5)]
    hdr = ("concept", "type", "trust", "state", "generated")
    for r in [hdr] + rows: print("  ".join(str(c).ljust(w[i]) for i, c in enumerate(r)))
    return 0

def cmd_new(a):
    rid = a.path if a.path.endswith(".md") else a.path + ".md"
    if os.path.basename(rid) in RESERVED: print("error: reserved filename"); return 1
    full = os.path.join(a.bundle, rid)
    if os.path.exists(full): print(f"error: {rid} exists"); return 1
    os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    q = lambda s: '"' + s.replace('"', '\\"') + '"' if re.search(r"[:#\[\]{},&*!|>'\"%@`]", s) else s
    fm = [f"type: {q(a.type)}"]
    if a.title: fm.append(f"title: {q(a.title)}")
    if a.desc: fm.append(f"description: {q(a.desc)}")
    if a.tags: fm.append("tags: [" + ", ".join(t.strip() for t in a.tags.split(",")) + "]")
    fm.append(f"generated: {{ by: {a.by}, at: {now} }}")
    with open(full, "w", encoding="utf-8") as fh:
        fh.write("---\n" + "\n".join(fm) + "\n---\n\n# " + (a.title or os.path.splitext(os.path.basename(rid))[0]) + "\n\n")
    print(f"created {rid}")
    return 0

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("bundle"); v.add_argument("--strict", action="store_true"); v.add_argument("--json", action="store_true"); v.set_defaults(f=cmd_validate)
    i = sub.add_parser("index"); i.add_argument("bundle"); i.add_argument("--write", action="store_true"); i.set_defaults(f=cmd_index)
    r = sub.add_parser("report"); r.add_argument("bundle"); r.set_defaults(f=cmd_report)
    n = sub.add_parser("new"); n.add_argument("bundle"); n.add_argument("path"); n.add_argument("--type", required=True)
    n.add_argument("--title"); n.add_argument("--desc"); n.add_argument("--tags")
    n.add_argument("--by", default="agent/unknown", help="actor: <producer>/<version> | human:<id> | process:<id>"); n.set_defaults(f=cmd_new)
    a = p.parse_args()
    sys.exit(a.f(a))

if __name__ == "__main__":
    main()
