#!/usr/bin/env python3
import pathlib
import re
import sys
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_LINK = re.compile(r"(?:href|src)=\"([^\"]+)\"")

SKIP_PREFIXES = ("http://", "https://", "mailto:", "tel:", "javascript:", "#", "data:")

files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
all_rel = {p.relative_to(ROOT).as_posix() for p in files}
issues = []
checked = 0

def normalize_target(source: pathlib.Path, link: str):
    link = link.strip()
    if not link or link.startswith(SKIP_PREFIXES):
        return None
    parsed = urlparse(link)
    path = parsed.path
    if not path:
        return None
    if path in {"/", "./", "."}:
        return None
    if path.startswith("/"):
        rel = path.lstrip("/")
    else:
        rel = (source.parent / path).resolve().relative_to(ROOT).as_posix()
    return rel

for f in files:
    rel = f.relative_to(ROOT).as_posix()
    if rel.startswith(".git/"):
        continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    links = []
    if f.suffix == ".md":
        links.extend(MD_LINK.findall(text))
    if f.suffix in {".html", ".xml"}:
        links.extend(HTML_LINK.findall(text))

    for raw in links:
        target = normalize_target(f, raw)
        if target is None:
            continue
        checked += 1
        # allow doc route query without checking query itself
        if target == "doc.html":
            continue
        if target not in all_rel:
            issues.append(f"{rel}: '{raw}' -> missing '{target}'")

if issues:
    print("Link check failed:")
    for line in issues:
        print(" -", line)
    sys.exit(1)

print(f"OK: checked {checked} internal links across {len(files)} files")
