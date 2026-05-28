#!/usr/bin/env python3
"""Extract a small structured receipt summary from OCR text."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


DATE_RE = re.compile(r"\b(\d{2})[./-](\d{2})[./-](\d{4})\b")
MONEY_RE = re.compile(r"(?:total|amount|sum|paid)\D{0,12}(\d+[.,]\d{2})", re.IGNORECASE)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_store(lines: list[str]) -> str:
    for line in lines:
        clean = normalize_space(line)
        if clean and not re.search(r"\d", clean):
            return clean.title()
    return "Unknown store"


def extract_receipt(text: str) -> dict[str, str | None]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    date_match = DATE_RE.search(text)
    total_match = MONEY_RE.search(text)
    return {
        "store": extract_store(lines),
        "date": "-".join(reversed(date_match.groups())) if date_match else None,
        "total": total_match.group(1).replace(",", ".") if total_match else None,
        "raw_text_length": str(len(text)),
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: receipt_ocr_postprocess.py <ocr-text-file>", file=sys.stderr)
        return 2
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    print(json.dumps(extract_receipt(text), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
