# Sefi Digital Studio storefront

The public storefront is intentionally fail-closed while product claims,
customer policies, checkout mapping, fulfillment, support, and evidence are
verified.

Every historical product route remains fail-closed. During the bounded
Creation Proof validation, `creation-proof.html` is the only permitted active
product page; it must contain exactly one Stripe payment link, truthful claims,
no analytics, and no interactive data collection. Git history preserves the
previous public surface for audit purposes.

Run the containment gate with:

```sh
python3 scripts/verify_containment.py
```
