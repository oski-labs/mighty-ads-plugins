---
name: inspect-brand-knowledge
description: Read and explain a Mighty brand's saved brand knowledge, including voice, audience, positioning, restrictions and source version. Use when customers ask what Mighty knows about their brand or how to edit that guidance.
---

# Inspect brand knowledge

Use the selected Mighty connection and the brand selected in this conversation,
including a selection made by the setup or management skill. Follow
[the setup skill](../setup/SKILL.md) for connection selection, brand resolution and
switching. Verify the brand against `list_organization_brands` for this connection.
An explicit brand in the current request takes precedence. If that named brand
is unavailable, do not substitute another brand; follow the setup skill's unavailable-brand handling.
If no brand is specified, retain the current selection when available; default to
the sole brand only when there is no existing selection to resolve. Ask for a
numbered choice when ambiguous. Never carry IDs or knowledge from another brand,
connection or conversation.

Call `get_brand_context` with the resolved brand's exact `org_brand_id`. Omit
revision_id for the latest knowledge; use a returned revision ID only when the
customer asks about that version.

Summarize the saved Markdown in plain language. It is customer-editable guidance,
not independent verification of claims or product availability. Explain missing
information without inventing it or substituting local files or
another brand's guidance. Product availability needs `list_brand_products`.

If no saved knowledge exists, offer a website for temporary campaign guidance
or setup in [Mighty's production console](https://console.mightyai.app). For a
website-based campaign, follow the management skill; do not call website findings
saved brand knowledge. Do not interpret a failed read as missing knowledge.
To edit or add knowledge in the console, select the brand, connect Google Drive
in Integrations, then open Brand context and refresh; or write and save directly.
This tool only reads; do not imply changes were saved. Keep document IDs and
revision numbers out of ordinary responses unless requested.
