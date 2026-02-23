#!/usr/bin/env python3
from __future__ import annotations

import argparse
import pathlib
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import parse_qs, urljoin, urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_BASE_URL = "https://damian545-dj.github.io/raport-publiczny/"
DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 3
USER_AGENT = "raport-publiczny-link-check/1.0 (+https://damian545-dj.github.io/raport-publiczny/)"

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_LINK = re.compile(r"(?:href|src)=\"([^\"]+)\"")
LOC_TAG = re.compile(r"<loc>([^<]+)</loc>")

SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "#", "data:")
SKIP_LOCAL_EXTENSIONS = {
    ".py",
    ".yml",
    ".yaml",
    ".sh",
    ".json",
    ".lock",
}
SKIP_PATH_FRAGMENTS = ("/actions/",)


@dataclass
class LinkRef:
    source_file: pathlib.Path
    line_no: int
    raw_url: str
    kind: str  # internal|external


@dataclass
class LinkError:
    source_file: pathlib.Path
    line_no: int
    raw_url: str
    message: str


class LinkChecker:
    def __init__(self, base_url: str, check_external: bool, timeout: int, retries: int):
        self.base_url = base_url if base_url.endswith("/") else base_url + "/"
        self.base_parsed = urlparse(self.base_url)
        self.base_path = self.base_parsed.path.rstrip("/") + "/"
        self.check_external = check_external
        self.timeout = timeout
        self.retries = retries

        self.files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
        self.existing_rel = {p.relative_to(ROOT).as_posix() for p in self.files}

        self.internal_refs: list[LinkRef] = []
        self.external_refs: list[LinkRef] = []
        self.errors: list[LinkError] = []

    def scan(self) -> None:
        for f in self.files:
            rel = f.relative_to(ROOT).as_posix()
            if rel.startswith(".git/"):
                continue
            text = f.read_text(encoding="utf-8", errors="ignore")
            lines = text.splitlines()
            for idx, line in enumerate(lines, start=1):
                urls = []
                if f.suffix == ".md":
                    urls.extend(MD_LINK.findall(line))
                if f.suffix in {".html", ".xml"}:
                    urls.extend(HTML_LINK.findall(line))
                if f.name == "sitemap.xml":
                    urls.extend(LOC_TAG.findall(line))

                for raw in urls:
                    self._register_ref(f, idx, raw.strip())

    def _register_ref(self, source: pathlib.Path, line_no: int, raw_url: str) -> None:
        if not raw_url or raw_url.startswith(SKIP_PREFIXES):
            return

        parsed = urlparse(raw_url)

        if parsed.scheme in {"http", "https"}:
            if any(fragment in parsed.path for fragment in SKIP_PATH_FRAGMENTS):
                return
            if parsed.netloc == self.base_parsed.netloc and parsed.path.startswith(self.base_path):
                self.internal_refs.append(LinkRef(source, line_no, raw_url, "internal"))
            else:
                self.external_refs.append(LinkRef(source, line_no, raw_url, "external"))
            return

        # Relative and root-relative paths are internal
        self.internal_refs.append(LinkRef(source, line_no, raw_url, "internal"))

    def check_internal(self) -> None:
        for ref in self.internal_refs:
            rel_path, query = self._resolve_internal_path(ref.source_file, ref.raw_url)
            if rel_path is None:
                continue

            # doc route query check
            if rel_path == "doc.html":
                target = parse_qs(query).get("file", [""])[0]
                if not target:
                    self.errors.append(LinkError(ref.source_file, ref.line_no, ref.raw_url, "missing ?file= parameter"))
                    continue
                if target not in self.existing_rel:
                    self.errors.append(LinkError(ref.source_file, ref.line_no, ref.raw_url, f"missing document '{target}'"))
                continue

            if pathlib.Path(rel_path).suffix in SKIP_LOCAL_EXTENSIONS:
                continue

            if rel_path not in self.existing_rel:
                self.errors.append(LinkError(ref.source_file, ref.line_no, ref.raw_url, f"missing file '{rel_path}'"))

    def _resolve_internal_path(self, source_file: pathlib.Path, raw_url: str) -> tuple[str | None, str]:
        parsed = urlparse(raw_url)

        if parsed.scheme in {"http", "https"}:
            # Base URL hosted path: /raport-publiczny/<file>
            hosted_path = parsed.path
            if hosted_path.startswith(self.base_path):
                hosted_path = hosted_path[len(self.base_path) :]
            elif hosted_path.startswith("/"):
                hosted_path = hosted_path[1:]
            path = hosted_path
            query = parsed.query
        else:
            path = parsed.path
            query = parsed.query

        if path in {"", "/", ".", "./"}:
            return None, query

        if path.startswith("/"):
            trimmed = path.lstrip("/")
            if trimmed.startswith("raport-publiczny/"):
                trimmed = trimmed[len("raport-publiczny/") :]
            return trimmed, query

        abs_path = (source_file.parent / path).resolve()
        try:
            rel_path = abs_path.relative_to(ROOT.resolve()).as_posix()
        except ValueError:
            return path, query
        return rel_path, query

    def check_external_urls(self) -> None:
        if not self.check_external:
            return

        seen: dict[str, tuple[bool, str]] = {}
        for ref in self.external_refs:
            if ref.raw_url not in seen:
                seen[ref.raw_url] = self._http_check(ref.raw_url)
            ok, reason = seen[ref.raw_url]
            if not ok:
                self.errors.append(LinkError(ref.source_file, ref.line_no, ref.raw_url, reason))

    def _http_check(self, url: str) -> tuple[bool, str]:
        last_err = "unknown error"
        for attempt in range(1, self.retries + 1):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method="GET")
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    code = getattr(resp, "status", 200)
                    if 200 <= code < 400:
                        return True, f"HTTP {code}"
                    last_err = f"HTTP {code}"
            except urllib.error.HTTPError as err:
                # 301/302 are not failures if they finally resolve to 200; urllib follows redirects,
                # so if we receive this error it is a final non-success status.
                last_err = f"HTTP {err.code}"
            except (urllib.error.URLError, socket.timeout, TimeoutError) as err:
                last_err = f"network error: {err}"
            except Exception as err:  # noqa: BLE001
                last_err = f"unexpected error: {err}"

            if attempt < self.retries:
                time.sleep(0.5 * attempt)

        return False, last_err

    def run(self) -> int:
        self.scan()
        self.check_internal()
        self.check_external_urls()

        if self.errors:
            print("Link check failed:")
            for err in sorted(self.errors, key=lambda e: (e.source_file.as_posix(), e.line_no, e.raw_url)):
                rel = err.source_file.relative_to(ROOT).as_posix()
                print(f" - {rel}:{err.line_no} -> {err.raw_url} :: {err.message}")
            print(f"\nSummary: {len(self.errors)} error(s) found")
            return 1

        print(
            "OK: checked "
            f"{len(self.internal_refs)} internal link reference(s) and "
            f"{len(self.external_refs) if self.check_external else 0} external link reference(s) "
            f"across {len(self.files)} files"
        )
        return 0


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Validate internal and optional external links")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL, help=f"Base GitHub Pages URL (default: {DEFAULT_BASE_URL})")
    p.add_argument("--check-external", action="store_true", help="Also check HTTP(S) external links")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help=f"HTTP timeout in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--retries", type=int, default=DEFAULT_RETRIES, help=f"HTTP retries (default: {DEFAULT_RETRIES})")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    checker = LinkChecker(
        base_url=args.base_url,
        check_external=args.check_external,
        timeout=args.timeout,
        retries=max(1, args.retries),
    )
    return checker.run()


if __name__ == "__main__":
    sys.exit(main())
