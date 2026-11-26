#!/usr/bin/env python3
"""Inventory the UI copy and measurement-relevant code hotspots in a web app.

Usage:
    python extract_ui_text.py <path> [--conditions flux,sdxl,...] [--min-len 12] [--out FILE]

Walks source files (tsx/jsx/ts/js/html/vue/svelte/json) and prints a Markdown report with:
  1. UI copy: string literals and JSX/HTML text nodes, with file:line
  2. Hotspots: code patterns that often matter for rating validity
     (randomization, defaults, sliders, required/disabled logic, storage writes,
     help modals, console logging, deselection)
  3. Condition-name hits: occurrences of each --conditions term, to look for blinding leaks

This is a finding aid. Read the source around each hit before reporting anything.
"""
import argparse
import os
import re
import sys

SOURCE_EXT = {".tsx", ".jsx", ".ts", ".js", ".mjs", ".html", ".htm", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", "coverage", "__pycache__", ".venv", "venv"}
MAX_FILE_BYTES = 1_500_000

HOTSPOTS = {
    "randomization": r"Math\.random|shuffle|seed|sort\(\s*\(\)\s*=>\s*Math\.random|crypto\.getRandomValues|latin",
    "biased-shuffle": r"sort\(\s*\(\)\s*=>\s*(0\.5\s*-\s*)?Math\.random\(\)\s*(-\s*0\.5)?",
    "defaults/preselected": r"defaultValue|defaultChecked|\bchecked\s*=\s*\{?\s*(true|\")|useState\(\s*\d",
    "slider": r"type\s*=\s*[\"']range[\"']|<Slider|slider",
    "required/disabled": r"\brequired\b|disabled\s*=|canGoNext|canSubmit|isComplete|allAnswered",
    "storage-write": r"\.create\(|\.update\(|\.insert\(|\.upsert\(|fetch\([^)]*(POST|PUT)|localStorage\.setItem|sessionStorage\.setItem|createRecord|updateRecord|setDoc|addDoc",
    "normalization": r"\bnorm\b|normali[sz]|\bpct\b|percent|/\s*\(?\s*max|\(\s*value\s*-\s*1\s*\)",
    "help/modal/tooltip": r"modal|tooltip|title\s*=|aria-describedby|popover|HelpModal|showHelp",
    "n/a-option": r"[\"']NA[\"']|N/A|not applicable|can'?t (judge|tell)|don'?t know|unsure",
    "deselect/toggle": r"deselect|uncheck|toggle",
    "position/order": r"ref-?left|ref-?right|left_?right|leftRight|\bposition\b|trial_?index|presentation_?order|display_?order|item_?order",
    "debug-output": r"console\.(log|debug|table)",
    "timing": r"Date\.now|performance\.now|timestamp|duration|elapsed",
}
POSITION_NOISE = re.compile(r"text-left|text-right|justify-left|items-left|ml-|mr-|pl-|pr-|left-\d|right-\d|border-l|border-r|rounded-l|rounded-r")

STRING_RE = re.compile(r"""(?P<q>["'`])(?P<s>(?:\\.|(?!(?P=q)).){1,2000}?)(?P=q)""")
JSX_TEXT_RE = re.compile(r">\s*([^<>{}\n][^<>{}]*?)\s*<")
CODEY = re.compile(r"^[\w./#:@\-\[\]()=]+$|^\s*$|^(flex|grid|text-|bg-|border|px-|py-|p-|m-|w-|h-|rounded|items-|justify-|gap-|space-)")


def iter_files(root):
    if os.path.isfile(root):
        yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in SOURCE_EXT:
                p = os.path.join(dirpath, fn)
                try:
                    if os.path.getsize(p) <= MAX_FILE_BYTES:
                        yield p
                except OSError:
                    pass


def looks_like_copy(s, min_len):
    s = s.strip()
    if len(s) < min_len:
        return False
    if CODEY.match(s):
        return False
    if " " not in s:
        return False
    # Tailwind class lists: mostly hyphenated tokens
    toks = s.split()
    if sum(1 for t in toks if "-" in t or ":" in t) > 0.6 * len(toks):
        return False
    if s.startswith(("http://", "https://", "data:", "SELECT ", "import ")):
        return False
    return sum(c.isalpha() for c in s) > 0.5 * len(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--conditions", default="", help="comma-separated condition/system names to search for")
    ap.add_argument("--min-len", type=int, default=12)
    ap.add_argument("--max-per-category", type=int, default=60)
    ap.add_argument("--out")
    args = ap.parse_args()

    conditions = [c.strip() for c in args.conditions.split(",") if c.strip()]
    copy_hits, hot_hits, cond_hits = [], {k: [] for k in HOTSPOTS}, {c: [] for c in conditions}
    hot_res = {k: re.compile(v, re.I) for k, v in HOTSPOTS.items()}

    for path in iter_files(args.path):
        rel = os.path.relpath(path, args.path) if os.path.isdir(args.path) else path
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError:
            continue
        is_json = path.endswith(".json")
        for i, line in enumerate(lines, 1):
            if len(line) > 3000:
                continue
            stripped = line.strip()
            if stripped.startswith(("//", "/*", "*", "#")) and not path.endswith((".html", ".htm")):
                comment = True
            else:
                comment = False
            if not is_json and not comment and "console." not in line:
                seen = set()
                for m in STRING_RE.finditer(line):
                    s = m.group("s")
                    if looks_like_copy(s, args.min_len) and s not in seen:
                        seen.add(s)
                        copy_hits.append((rel, i, s.strip()))
                for m in JSX_TEXT_RE.finditer(line):
                    s = m.group(1)
                    if looks_like_copy(s, args.min_len) and s not in seen:
                        seen.add(s)
                        copy_hits.append((rel, i, s.strip()))
            for k, r in hot_res.items():
                if r.search(line):
                    if k == "position/order" and POSITION_NOISE.search(line) and not re.search(r"ref-left|ref-right|order\b|trial", line, re.I):
                        continue
                    hot_hits[k].append((rel, i, stripped[:160]))
            for c in conditions:
                if re.search(re.escape(c), line, re.I):
                    cond_hits[c].append((rel, i, stripped[:160]))

    out = []
    out.append(f"# UI inventory for `{args.path}`\n")
    out.append("Finding aid only: read the surrounding source before reporting.\n")
    out.append(f"## 1. UI copy ({len(copy_hits)} strings)\n")
    last = None
    for rel, i, s in copy_hits:
        if rel != last:
            out.append(f"\n### {rel}\n")
            last = rel
        out.append(f"- L{i}: {s}")
    out.append("\n## 2. Hotspots\n")
    for k, hits in hot_hits.items():
        out.append(f"\n### {k} ({len(hits)})\n")
        for rel, i, s in hits[: args.max_per_category]:
            out.append(f"- `{rel}:{i}` {s}")
        if len(hits) > args.max_per_category:
            out.append(f"- ... {len(hits) - args.max_per_category} more")
    if conditions:
        out.append("\n## 3. Condition-name occurrences (check for blinding leaks)\n")
        for c, hits in cond_hits.items():
            out.append(f"\n### `{c}` ({len(hits)})\n")
            for rel, i, s in hits[: args.max_per_category]:
                out.append(f"- `{rel}:{i}` {s}")
            if len(hits) > args.max_per_category:
                out.append(f"- ... {len(hits) - args.max_per_category} more")

    text = "\n".join(out) + "\n"
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"wrote {args.out} ({len(copy_hits)} strings)", file=sys.stderr)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
