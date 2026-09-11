from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
HTML_FILES = sorted(ROOT.glob("*.html"))
ACTIVE_PRODUCT = ROOT / "creation-proof.html"

REQUIRED_TEXT = (
    "Sefi Digital Studio is temporarily unavailable.",
    "No products are currently offered for sale",
    'name="robots" content="noindex, nofollow, noarchive"',
)

BANNED_LEGACY_PATTERNS = {
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

ACTIVE_REQUIRED_TEXT = (
    "Creation Proof",
    "$29.00 USD",
    "one-time purchase",
    "Files stay on your computer",
    "does not guarantee monetization or appeal approval",
    "Delivered to the email used at checkout within one business day",
    'name="robots" content="noindex, nofollow, noarchive"',
)
ACTIVE_BANNED_PATTERNS = {
    "unsupported outcome claim": re.compile(
        r"(?:appeal[- ]?proof|monetization[- ]?safe|guaranteed approval|"
        r"guaranteed monetization|success rate|income|earnings)",
        re.IGNORECASE,
    ),
    "unapproved urgency or scarcity": re.compile(
        r"(?:limited time|only \d+ left|countdown|ends (?:today|tonight)|"
        r"act now|sale ends)",
        re.IGNORECASE,
    ),
    "analytics or active code": re.compile(
        r"(?:googletagmanager|google-analytics|gtag\s*\(|fbq\s*\(|"
        r"webhook|fetch\s*\(|xmlhttprequest|<form\b)",
        re.IGNORECASE,
    ),
    "unresolved checkout": re.compile(r"__CHECKOUT_URL__"),
}
ALLOWED_ACTIVE_LINK_HOSTS = {
    "buy.stripe.com",
    "support.google.com",
}


def main() -> int:
    if not HTML_FILES:
        raise SystemExit("No HTML routes found")

    expected = (ROOT / "maintenance.html").read_text(encoding="utf-8")
    failures: list[str] = []

    for path in HTML_FILES:
        if path == ACTIVE_PRODUCT:
            continue
        text = path.read_text(encoding="utf-8")
        if text != expected:
            failures.append(f"{path.name}: does not match maintenance.html")
        for required in REQUIRED_TEXT:
            if required not in text:
                failures.append(f"{path.name}: missing required containment text")
        for label, pattern in BANNED_LEGACY_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{path.name}: contains {label}")

    if not ACTIVE_PRODUCT.is_file():
        failures.append("creation-proof.html: active product page is missing")
    else:
        active = ACTIVE_PRODUCT.read_text(encoding="utf-8")
        for required in ACTIVE_REQUIRED_TEXT:
            if required not in active:
                failures.append(
                    f"creation-proof.html: missing required product boundary"
                )
        for label, pattern in ACTIVE_BANNED_PATTERNS.items():
            if pattern.search(active):
                failures.append(f"creation-proof.html: contains {label}")
        hrefs = re.findall(r'href="([^"]+)"', active)
        stripe_links = [
            href for href in hrefs if urlparse(href).netloc == "buy.stripe.com"
        ]
        if len(stripe_links) != 1:
            failures.append(
                "creation-proof.html: requires exactly one Stripe checkout link"
            )
        for href in hrefs:
            if urlparse(href).netloc not in ALLOWED_ACTIVE_LINK_HOSTS:
                failures.append(
                    f"creation-proof.html: unapproved link destination: {href}"
                )

    if failures:
        raise SystemExit("\n".join(failures))

    print(
        f"Containment verified across {len(HTML_FILES) - 1} legacy routes; "
        "Creation Proof is the only active product"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
