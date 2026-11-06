---
name: weekly-ads-review
description: Review recent advertising performance across connected channels when a merchant asks how ads performed, what changed week over week, for a weekly ads summary, or what needs attention now.
---

# Weekly ads review

Read [the analysis principles](../references/ads-analysis-principles.md) and
[response pattern](../references/workflow-response-pattern.md). For each selected
channel, read only its existing reference: [ChatGPT Ads](../manage-ads/references/chatgpt-ads.md),
[Google Ads](../manage-ads/references/google-ads.md),
[Meta Ads](../manage-ads/references/meta-ads.md) or
[Reddit Ads](../manage-ads/references/reddit-ads.md).

Resolve the brand and requested channels through the existing setup and
`manage-ads` rules. If the user did not name a channel, check readiness and review
the connected advertising channels. Do not make an unavailable channel a blocker;
name it only when its absence changes the requested comparison.

Use the dates the user supplied. Otherwise compare the most recent seven complete
account-local days with the preceding seven complete days. Keep periods, filters,
attribution and conversion definitions aligned. Exclude today unless the user
explicitly asks for it, and label any period that remains partial.

Start at campaign level using the channel's performance tool. Select the KPI from
each campaign objective, not one universal ROAS rule. Recompute rates from totals.
Only drill into ads, search terms, audiences or placements when a material change
needs an explanation; this is triage, not every deep audit at once.

Quietly determine coverage. A useful review can proceed with one connected channel
or without every metric. State a missing conversion event, incomplete page or
incomparable attribution only when it changes the verdict. Provider-reported
conversions remain separate across channels unless their definitions align.

Return:

- One sentence describing the most important change.
- A compact current-period versus previous-period comparison for the metrics that
  drive the decision.
- At most three drivers or exceptions, naming the campaign or channel and why it
  matters.
- At most three actions under **Do now**, **Test next** or **Watch**. Route deeper
  work to the relevant focused workflow when useful.

Do not manufacture an action in a stable week. Offer a shareable weekly summary
only when the user needs to send or preserve the review. Read-only analysis needs
no confirmation; any selected change follows `manage-ads` and the channel's write
rules.
