# Amazon Ads

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_amazon_ads_readiness` to find its Amazon
Ads connections. Each connection is one advertising profile: one advertiser
account in one marketplace, so a brand selling in several countries has several.
Show them as numbered choices with account name, type and marketplace if more
than one exists; reuse the selected `connection_id` and `org_brand_id` for every
subsequent call. Never guess profiles or switch brands on a permission failure.
Direct missing or revoked access to the brand's Amazon Ads integration; do not
request credentials.

Readiness confirms the saved profile with a live read and reports whether the
connection holds management permission. A read-only connection cannot be
elevated by asking; reconnecting with management access is a Console step and
also needs edit permission on the profile in Amazon. Readiness names the date
Amazon's yearly consent expires when it is within a month: tell the customer to
reconnect in Integrations before then.

Amazon tools cover Sponsored Products only: reads, reports, paused campaign and
ad group creation, daily budget changes and pause/enable. Sponsored Brands,
Sponsored Display and DSP are not available; say so rather than guessing. Never
route Amazon requests through Meta, Google or ChatGPT tools.

## Inventory

Use `list_amazon_campaigns` / `get_amazon_campaign`, then
`list_amazon_ad_groups` / `get_amazon_ad_group`, `list_amazon_product_ads` and
`list_amazon_targets`. Use the campaign or ad-group filter when known. Show
names and customer-facing statuses in short numbered lists, keeping the mapping
stable across follow-ups. IDs stay internal unless requested. Follow
`next_cursor` with unchanged connection, filters and page size; a page is one
provider page, not the complete inventory, and an empty page does not prove
there are no other pages. Lists show enabled and paused items only; details can
still return archived ones.

Budgets and bids are amounts in the profile's currency as Amazon stores them:
`daily_budget` 25.5 USD is $25.50 per day. `state` is what the advertiser set;
`delivery_status` and `delivery_reasons` explain why an item is not delivering,
for example `CAMPAIGN_PAUSED`, `CAMPAIGN_OUT_OF_BUDGET`, `OUT_OF_STOCK`,
`NOT_IN_BUYBOX` or `ADVERTISER_PAYMENT_FAILURE`. A `targeting_type` of `AUTO`
means Amazon chooses targets; `MANUAL` campaigns use the keyword, product and
category targets you can list. Product ads show the advertised product as an
ASIN for vendors or a SKU for sellers, with the resolved ASIN when Amazon
returns it; titles and images are not included. Targets show keywords with
match type, product or category targets, auto-targeting themes and negatives
(`negative` true, at ad-group or campaign level); they describe configuration,
not the search terms that matched.

## Spend and results

Amazon only reports performance through asynchronous reports, and it limits
report jobs for all Mighty customers together, so run one report per question:

1. Call `get_amazon_report` with `report`: campaign-local `start_date` and
   `end_date_exclusive` (1–120 days), `level` campaign or ad_group,
   `granularity` total or daily, and optional `campaign_ids` or `ad_group_ids`
   from the inventory tools. Keep the returned `report_handle`.
2. Call `get_amazon_report` with `report_handle` alone to check status, about
   once a minute and at most a few times in one turn. `COMPLETED` is ready;
   `FAILED` is final, so run a smaller report instead of polling again.
3. Call `get_amazon_report` with `report_handle` and `read_results=true`, then
   follow `next_cursor` as `after` with the same handle, connection and page
   size before quoting totals.

If submission fails with a rate-limit message, wait the reported time or try
later; never resubmit in a loop, and never resubmit a report whose outcome is
unknown without telling the customer. Handles expire after 24 hours.

Report rows cover only the selected connection's marketplace, even when the
advertiser runs campaigns in other countries under the same Amazon account.
If rows have invalid or missing campaign IDs, every page warns how many were
omitted. Keep the valid rows, disclose the omission and do not quote complete totals.
Rows carry impressions, clicks, `cost`, `ctr` (Amazon's percentage), `cpc`,
`purchases`, `purchases_promoted`, `sales`, `sales_promoted`, `units_sold` and
`roas`, with money in each row's `currency_code`. Purchases and sales use
Amazon's default attribution window: seven days for sellers and fourteen days
for vendors, counted on the day of the ad interaction, and they include related
("halo") products unless the promoted variant is used. Amazon restates
conversions for up to 60 days and delivers impressions and clicks within about
12 hours, so treat the last few days as provisional. `missing_metrics` lists
fields Amazon did not return; they are unknown, not zero. Sales are
Amazon-attributed order value, not store revenue.

## Create campaigns and ad groups

Changes need a management connection: `management_permission_granted` true in
readiness. Otherwise say the connection is read-only and that reconnecting with
management access in Integrations is a Console step; never ask for credentials.

Use the chosen products from `list_brand_products` only to plan; product ads
and targets cannot be added yet, so a new campaign cannot deliver until the
customer adds them in the Amazon Ads console or a later Mighty release. Say so
before approval. Ask only for missing settings: name (unique in the profile),
daily budget in the profile currency, automatic or manual targeting, bid
strategy (fixed bids, dynamic down only, or dynamic up and down; do not choose
for the customer), and an optional start day and inclusive last day in the
marketplace's time zone. Explain that a daily budget is Amazon's cap for that day, not a
spend promise.

Show one compact plan with the brand, profile (account name and marketplace),
settings and the delivery caveat. Say that the campaign and any ad group start
paused and activation needs separate approval. One approval covers that exact
plan; ask again only if settings change.

1. Call `create_amazon_campaign` with the `connection_id` and approved settings.
2. Read `get_amazon_campaign` and pass its `status_state` as
   `expected_campaign_state` to `create_amazon_ad_group` with the approved name
   (unique in the campaign) and default bid in the profile currency. The
   campaign must still be paused.
3. Inspect the created items and report confirmed names and paused states. If
   part of the plan failed, report the completed items and stop dependent
   creation.

Keep IDs and state tokens inside tool calls; the customer chooses by
names or numbered selections. Never ask them for technical identifiers.

## Change budgets or status

Read details immediately before proposing a change and pass the token the
change needs: `budget_state` for a budget change, `status_state` of the
selected item for a pause or activation. Each token covers only what that
change depends on, so a pause is never refused because the budget or name
changed. Show the exact target and old → new setting with spend or delivery
impact, then ask for approval.

- `update_amazon_campaign_budget` changes one campaign's daily budget. An
  enabled campaign may spend up to the new amount the same day. Campaigns
  without a daily budget are changed in the Amazon Ads console.
- `set_amazon_status` enables or pauses exactly one campaign or ad group;
  archiving is never offered. Enabling a campaign may resume its already-enabled
  ad groups, ads and targets; paused ones stay paused. Enabling an ad group in a
  paused campaign does not deliver. Before campaign activation approval, list
  its ad groups and product ads, name what could resume and what stays paused,
  and warn that out-of-stock or ineligible products still will not serve. If
  the inventory is incomplete, narrow it before approval. Enable ad groups
  before the campaign; pause the campaign first when stopping a setup. Refresh
  detail states between writes and stop dependent activation on a failed or
  uncertain step.

## Boundaries and recovery

Readiness verifies profile access only, not measurement or launch readiness.
Product ads, targets, negative targets, archiving, deletion and bid strategy
changes are not available; if asked, say the change is not available yet and
offer the Amazon Ads console.

Amazon has no validation call and no idempotency key, so never retry a write
automatically. `verified` means the requested settings were read back;
`unchanged` means nothing needed to change. For `rejected`, nothing was saved:
explain the reason from the safe message and give a next step; a duplicate name
means inspect the existing item, not rename and retry. For
`confirmation_pending`, Amazon accepted the change but its saved settings are
unconfirmed; for `uncertain`, Amazon never answered and the result names the
campaign or ad group. In both cases check the item at most twice with the list
tools filtered to the campaign (match by name for an uncertain creation), report
what is known, and ask the customer to check the Amazon Ads console before
another write. A stale token means the setting it guards changed: read the item again and
reconfirm the plan rather than replaying it.

On a rate-limit error, wait the reported time before retrying or narrow the
request; never retry in a loop. If a read fails after profile access changed,
direct the customer to Reconnect on the Amazon Ads integration. Never present a
partial page as the whole profile, invent totals, or quote raw provider codes.
