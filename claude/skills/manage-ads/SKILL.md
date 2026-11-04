---
name: manage-ads
description: Inspect Meta Ads, Google Ads and ChatGPT Ads through MightyAI, research Google Search keywords and forecasts, find products, create paused Meta photo, Google Search and ChatGPT campaigns and ads, and manage supported Meta, Google and ChatGPT settings. Meta supports reads, paused photo creation, guarded settings edits and explicit pause/activation.
---

# Manage ads

Use the user's selected Mighty connection and resolve its available brands with
`list_organization_brands`. Match an explicit brand name or the current
conversation's selected brand against that returned list. An explicit requested
brand takes precedence: select a unique match for reads and state the brand; if
it is absent, follow the setup skill's unavailable-brand handling and do not read
another brand. Default to the sole available brand only when no brand is specified
and there is no existing conversation selection to resolve. Ask for a numbered
choice when the request is ambiguous. Keep the selected brand specific
to this conversation and pass its exact `org_brand_id` to every subsequent tool.
Follow the setup skill when switching brands. Never guess IDs, request
credentials, or carry provider-account selections or write approval across brands.

For ChatGPT Ads, read [its channel reference](references/chatgpt-ads.md).
For Google Ads, read [its channel reference](references/google-ads.md).
For Meta Ads, read [its channel reference](references/meta-ads.md). Use its read tools
for inventory and performance, and its separate photo-creation tools after approval.
Use its editing context and edit/status tools for separately approved changes; creative replacement is unavailable.
Never apply Google or ChatGPT write tools to Meta requests.
Use the channel the user names; ask if ambiguous rather than silently switching.
Google creation and changes support Search only. Use the selected channel’s tools.
Use live provider reads, not remembered data or published draft workspaces.
Read-only requests require no change confirmation.

For conversion counts, use the selected ads provider's reporting for the exact
campaign and dates. Label provider-reported conversions separately from
Mighty-attributed Shopify paid orders; they measure different attribution.
Answer whether conversions were reported before explaining measurement gaps.
Missing or failed provider data is unknown, not zero. A decline needs comparable
periods; a count alone does not explain its cause. Follow the channel reference
for the reporting tool and attribution details.

When choosing products for ads, use names or links the user already supplied.
Otherwise ask: “Do you have products in mind, or would you like me to suggest some?”
Use `list_brand_products` to check supplied products or find candidates. If asked
for suggestions, show a short numbered list with reasons tied to the campaign
goal; do not invent bestseller claims. Let the user choose before creating ads.
Flag unknown availability or shipping checks rather than claiming readiness.

Before drafting ordinary ad copy yourself, read `get_brand_context` for the latest
saved guidance. Quick Campaign uses `prepare_chatgpt_campaign` or `prepare_meta_campaign` for the
selected channel; each reads that
same current context and returns generated copy; do not make a duplicate context
read. Use the returned voice, audience and restrictions.
If a successful read confirms no saved context, offer two numbered choices:

1. Share a website to prepare the campaign from public information.
2. Add guidance in [Mighty's production console](https://console.mightyai.app):
   select the brand, connect Google Drive in Integrations, then open Brand context
   and refresh; or write and save context directly.

Reuse an already supplied website. Read it with the host's browsing tools when
available; use `list_brand_products` for product evidence. If it cannot be read,
ask for relevant website text and product links. Explain that website-based copy
needs their review for tone, audience and claims. Use it only in this conversation;
do not save it as shared context. Setup is optional. An access/read failure is
not missing context; resolve that failure rather than bypassing it.
For creation, collect only missing required settings and invite optional campaign
context once. Ground copy and destinations in the chosen products and brand facts.
Show one compact plan: brand, campaign/group/ad counts, budget, bids, geography,
schedule, copy and product destinations. Say “All new items will be paused;
activation needs separate approval.” One approval covers those exact items,
including selected creative and any images; do not ask again per item unless the plan or relevant
settings change. Existing active ads can keep spending. Follow the channel reference.
Keep prices, offers and benefits tied to the selected product; brand examples
may describe other products. Show the proposal with specific uncertainties flagged
beside the affected copy and suggest a correction; resolve those before creation.

For reads and changes, show short numbered lists with names and statuses; number
ads too when selection is needed. Accept `2`, `1 and 3`, or `all` against the
displayed list; keep its mapping stable and clarify ambiguous selections.
Ask only for missing inputs. Read-only selections do not authorize writes.
For ChatGPT spend-review questions, use `get_chatgpt_spend_opportunities` with a campaign ID for a selected
campaign, or without a campaign ID for the whole account.
Separate historical findings from returned live pause
recommendations and conditional savings estimates. Do not call a weaker CTR
signal proven waste or guaranteed savings. Do not turn a read recommendation
into a status or bid change without the user's explicit request and confirmation.
For bidding, no recommendations or automatic strategy selection.
Use customer language: campaign/ad group/ad, not parent/child or hierarchy.
Translate tool results/errors; do not quote technical messages. Keep IDs and
timestamps out unless requested. Say “I checked,” not “live readback.”

Show the exact selected targets and old → new settings, including live-delivery
impact, and ask for confirmation. Apply only those confirmed changes, once per
target. Report what changed, what still prevents ads from running and the next step.
Some selected changes can succeed while others fail; report them separately.
If settings changed, check them again and reconfirm. If the result cannot be
confirmed, follow the channel's bounded read-only checks. Explain what changed,
what remains unknown and the next safe step; never retry writes automatically.
Finish with confirmed counts/statuses and one useful next step, not technical logs.
Do not claim all items are paused, running or spending nothing without evidence.
