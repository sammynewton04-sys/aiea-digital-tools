# Sefi Digital Studio storefront

The public storefront is intentionally fail-closed while product claims,
customer policies, checkout mapping, fulfillment, support, and evidence are
verified.

No product, subscription, trial, checkout, payment link, analytics tag, or
customer notification is active in this repository. Every historical HTML
route serves the same neutral maintenance page. Git history preserves the
previous public surface for audit purposes.

Run the containment gate with:

```sh
python3 scripts/verify_containment.py
```
