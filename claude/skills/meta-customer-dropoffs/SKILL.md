---
name: meta-customer-dropoffs
description: Diagnose where Meta-attributed customers drop between ad attention, landing-page activity and purchase when a merchant asks why clicks are not converting or where the funnel breaks.
---

# Meta customer drop-offs

Read [the analysis principles](../references/ads-analysis-principles.md),
[response pattern](../references/workflow-response-pattern.md), and
[Meta reference](../manage-ads/references/meta-ads.md).

Resolve the brand, Meta connection, exact campaign scope and dates. Identify the
campaign objective, optimization goal and conversion event before judging the
funnel. Use a consistent action definition and attribution window throughout.

At the most useful supported level, compare the available sequence:

1. Impressions or video attention.
2. Link or outbound clicks.
3. Landing-page views.
4. Add-to-cart activity.
5. Checkout activity.
6. Purchases or the campaign's intended conversion.

Keep all clicks separate from link and outbound clicks. Do not combine website,
omni and total variants of the same purchase event. Missing or privacy-limited
events are unknown, not zero. Meta provides aggregate attributed events, not raw
visitor journeys; a gap signals where to investigate but does not prove a page,
offer or checkout defect.

Find the largest supported drop that is both material and sufficiently measured.
Then identify the likely owner of the next check:

- weak attention or outbound response → creative or audience;
- clicks without landing-page views → destination speed, redirect or tracking;
- landing views without cart/lead action → message, product, offer or page;
- cart without checkout/purchase → checkout, pricing, shipping or measurement;
- sudden event disappearance → tracking or reporting before optimization.

Lead with the stage that deserves attention, the exact supporting counts/rates,
and a short why. Give one concrete verification or test before proposing several
optimizations. Use the creative-health or audience workflow when the evidence
points there. This analysis changes nothing. Prepare the next action; apply a
supported Meta change only through the [manage-ads workflow](../manage-ads/SKILL.md)
after approval, and never claim the site or campaign was changed.
