from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html"))

REQUIRED_TEXT = (
    "Sefi Digital Studio is temporarily unavailable.",
    "No products are currently offered for sale",
    'name="robots" content="noindex, nofollow, noarchive"',
)

BANNED_PATTERNS = {
    "payment destination": re.compile(
        r"(?:buy\.stripe\.com|checkout|payment[_ -]?link|apple\s*pay|google\s*pay)",
        re.IGNORECASE,
    ),
    "price or currency amount": re.compile(
        r"(?:[$€£]\s*\d|\b(?:usd|cad|eur|gbp)\b|/\s*mo(?:nth)?)",
        re.IGNORECASE,
    ),
    "unsupported commercial claim": re.compile(
        r"(?:1,420\+|best seller|verified direct|resell rights|instant delivery|"
        r"hands[- ]?free|100% autonomous|unlimited|24/7 support|zero credit)",
        re.IGNORECASE,
    ),
    "analytics or notification code": re.compile(
        r"(?:googletagmanager|google-analytics|gtag\s*\(|fbq\s*\(|pixel|"
        r"notification|webhook|fetch\s*\(|xmlhttprequest)",
        re.IGNORECASE,
    ),
    "interactive selling control": re.compile(
        r"<(?:a|button|form|input|select|textarea)\b",
        re.IGNORECASE,
    ),
}


def main() -> int:
    if not HTML_FILES:
        raise SystemExit("No HTML routes found")

    expected = (ROOT / "maintenance.html").read_text(encoding="utf-8")
    failures: list[str] = []

    for path in HTML_FILES:
        text = path.read_text(encoding="utf-8")
        if text != expected:
            failures.append(f"{path.name}: does not match maintenance.html")
        for required in REQUIRED_TEXT:
            if required not in text:
                failures.append(f"{path.name}: missing required containment text")
        for label, pattern in BANNED_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{path.name}: contains {label}")

    if failures:
        raise SystemExit("\n".join(failures))

    print(f"Containment verified across {len(HTML_FILES)} HTML routes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
