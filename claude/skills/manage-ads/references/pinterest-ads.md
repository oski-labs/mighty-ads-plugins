# Pinterest Ads

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_pinterest_ads_readiness` to find its
Pinterest Ads connections. Show account names as numbered choices if more than
one exists; reuse the selected `connection_id` and `org_brand_id` for every
subsequent call. Never guess accounts or switch brands on a permission failure.
Direct missing or revoked access to the brand's Pinterest Ads integration; do
not request credentials.

Readiness reads the saved ad account and checks the connecting Pinterest user's
current business-access role. If that role was removed, or Pinterest refused
the saved authorization, readiness says so in `next_step` instead of failing:
relay it and point the customer to the Pinterest business owner or to
Reconnect. A read-only connection cannot be elevated by asking; reconnecting
with management access is a Console step. `write_access_checked` is always
false: readiness does not test changes. `rate_limit.remaining` is Pinterest's
remaining request budget for this app: when it is low, say so and avoid
unnecessary reads. `refresh_token_expires_at` is when the saved grant would
expire; Mighty renews it daily, so mention it only when `next_step` does.

Reads change nothing. Pinterest's developer rules forbid taking actions without
the customer specifically considering each one, so never run or suggest
automatic optimisation loops on Pinterest; every change needs its own
approval. Never route Pinterest requests through Meta, Google, Reddit,
Snapchat or ChatGPT tools. Ads, Pins, catalogs, shopping campaigns, audiences,
targeting beyond countries, archiving and deletion are not available here.

## Inventory

Use `list_pinterest_campaigns` / `get_pinterest_campaign`, then
`list_pinterest_ad_groups` / `get_pinterest_ad_group`, then
`list_pinterest_ads` / `get_pinterest_ad`. Lists come newest first. Use the
campaign or ad-group filter when known, and `include_archived` only when the
customer asks about archived items. Show names and statuses in short numbered
lists, keeping the mapping stable across follow-ups. IDs stay internal unless
requested. Follow `next_cursor` with unchanged connection, filters and page
size; a page is not the complete inventory, and an empty page does not prove
there are no other pages. A positive `skipped_items` means Pinterest returned
rows that could not be read: say the list is incomplete.

Budgets, bids and spend caps are Pinterest micro-currency amounts in the
account currency (1,000,000 per unit): show `daily_spend_cap` 50000000 USD as
$50.00. A campaign with `is_campaign_budget_optimization` true holds the budget
itself (its ad groups show `budget_type` CBO_ADGROUP); otherwise each ad group
has its own daily or lifetime budget. `status` (ACTIVE, PAUSED or ARCHIVED) is
what the account set. `summary_status` is Pinterest's computed state, for
example RUNNING, PAUSED, NOT_STARTED, COMPLETED or ADVERTISER_DISABLED, and for
ads APPROVED, PENDING or REJECTED; translate it into plain words and name a
paused parent when a child is paused by it. An ad's `review_status`,
`rejected_reasons` and `rejection_labels` explain ad review. Ad groups carry
configured targeting and `auto_targeting_enabled` (Pinterest Performance+
targeting expansion); ads carry the promoted Pin ID but not Pin content.
Timestamps are Unix seconds in UTC.

## Spend and results

Use `get_pinterest_performance` with explicit inclusive UTC `start_date` and
`end_date` within the last 90 days (at most 90 days): `granularity=total` or
`daily`. Days are UTC because that is Pinterest's API default; Ads Manager shows
the account's time zone, so say that day totals at the edges can differ.
Choose the level:

- `account`: account totals from Pinterest's account report.
- `campaign`: every campaign including archived ones, newest first, or up to
  25 `entity_ids`.
- `ad_group` or `ad`: up to 25 `entity_ids`, or a `campaign_id` (and
  `ad_group_id` for ads) to page through that parent's items, archived ones
  included so spend before archiving is not lost.

Follow `next_cursor` before quoting totals. A daily page holds at most 2,000
rows; use fewer days or a smaller `limit` if asked.

Metrics are spend, paid and total impressions, Pin clicks, outbound clicks,
engagements, saves, click-through rate, conversions, checkouts and checkout
value, page visits, signups, leads, video views and completions. `spend` and
`checkout_value` are already in the account currency (`currency_code`); the
`_micro` fields keep the raw amount. Paid metrics count the ad itself; total
metrics add earned activity from saved Pins, which Pinterest does not bill.
Conversions are Pinterest-attributed Tag or Conversions API events using 30-day
click, 30-day engagement and 1-day view attribution by the time of the ad
action; they are not store orders, and checkout value is not store revenue.
`missing_metrics` lists metrics Pinterest did not return; they are unknown, not
zero. A day with no row had no reported delivery. Pinterest can restate recent
days, so label the last two days as provisional.

## Boundaries and recovery

Readiness verifies account access and the role only, not the Pinterest Tag,
measurement or launch readiness. If event evidence is insufficient, say so and
recommend Pinterest Tag or Conversions API setup in Pinterest Ads Manager.

On a rate-limit error, wait the stated time before retrying or narrow the
request; never retry in a loop. Pinterest limits the whole app, so a limit
reached by another customer can affect this one. If a read fails after account
access changed, direct the customer to Reconnect on the Pinterest Ads
integration card. Never present a partial page as the whole account, invent
totals, or quote raw provider codes.

## Create paused campaigns and ad groups

1. Resolve the brand and connection with `check_pinterest_ads_readiness`; it must
   show a manage connection with `management_permission_granted`. Read-only
   connections cannot be elevated by asking; reconnecting with management access
   happens in Console.
2. Collect the campaign name and objective: website traffic (Pinterest's
   CONSIDERATION objective, billed per click) or awareness (billed per
   impression). Decide with the customer who holds the budget and pass the
   choice as `campaign_budget_optimization`: false gives each ad group its own
   daily or lifetime budget and the campaign no cap; true makes the campaign
   hold exactly one daily or lifetime spend cap (a lifetime cap needs an end
   time) and its ad groups no budget. Pinterest refuses ad-group budgets for
   newer advertisers (error 2454, "CBO required"); when a creation is rejected
   with that code, offer the campaign-budget form. The choice cannot be changed
   later. Optional future start and
   end times; Pinterest starts immediately otherwise. For each ad group collect
   the name, budget (type and amount, unless the campaign holds the budget),
   bidding (automatic, or a maximum or target bid with an amount), upper-case
   country codes, whether Pinterest Performance+ targeting expansion stays on
   (Pinterest's default; say what it does), and optional dates inside the
   campaign's, which are not available when the campaign holds the budget.
   Amounts are micro-currency (1,000,000 per unit); show readable amounts and
   say what you will send. Pinterest enforces its own minimums and reports
   them in the result when it refuses.
3. Present one compact plan: campaign name, objective, budget mode, dates and
   cap, then each ad group with budget, bidding, countries, targeting expansion
   and dates. Say: "All new items will be paused. Activation requires separate
   approval." Obtain approval of that exact plan before any creation.
4. Call `create_pinterest_campaign`. Pass the returned `item` (or a fresh
   `get_pinterest_campaign` item) unchanged as `campaign` to
   `create_pinterest_ad_group`; the campaign must still be paused. New ad groups
   have no ads, so they cannot serve; ads are created in Pinterest Ads Manager
   for now. Relay the result's warnings.

## Change settings and status

1. Read `get_pinterest_edit_context` for the target campaign, ad group or ad and
   pass its `account` and `item` unchanged; do not edit or rebuild the item.
   Each change compares the item with a fresh read and reads it again
   immediately before sending, so another edit to the settings it changes makes
   Mighty refuse it without sending anything, while unrelated edits do not block
   it. Pinterest itself offers no precondition: a change made in the moment
   between that last read and the request can be overwritten, and verified
   results say so.
2. Present a before/after plan naming the affected item, readable amounts in
   the account currency and the delivery impact, and get approval of that exact
   plan. When a campaign's start moves later or its end earlier, also name the
   ad groups from the editing context's `ad_groups` whose own dates reach past
   the new schedule: they wait for the campaign to start, stop when it ends, or
   cannot run at all when their dates fall outside it. Pass their IDs as
   `affected_ad_group_ids`; Mighty refuses the change if the affected set has
   changed since. If the context says the ad groups could not be read, do not
   plan such a change.
3. Use `update_pinterest_campaign` for a campaign's name, its existing daily or
   lifetime spend cap (only when the campaign holds the budget), start or end
   time, or to remove the end time. Use `update_pinterest_ad_group` for an ad
   group's name, the amount of its existing daily or lifetime budget, bid
   strategy and bid, or dates; switching to automatic bidding removes the bid,
   the budget type cannot change, and an ad group whose campaign holds the
   budget has no budget or dates of its own. New start times must be in the
   future and ad-group dates must stay inside the campaign's. Automated and
   Performance+ campaigns are changed in Pinterest Ads Manager.
4. Use `set_pinterest_status` only after explicit approval of the exact target
   and the desired ACTIVE or PAUSED state. Activation may start real spend and
   changes only the selected item: activating a campaign does not activate its
   ad groups or ads, and the result names paused campaigns and ad groups that
   still block delivery, an ad's review state and Pinterest's computed
   `summary_status`. Activation is refused, with nothing sent, if the item's
   budget (including its mode), bid or schedule changed since it was read; read
   it again and get
   approval of the current values. A pause depends only on the item's status.
   To stop delivery, pause the campaign first.

Results report `verified`, `unchanged`, `rejected` (Pinterest refused, so nothing
was applied; the message relays Pinterest's reason, such as a budget minimum),
`confirmation_pending` (accepted but not yet confirmed) or `uncertain` (the
submission may or may not have applied). When Mighty refused because the
settings changed since they were read, read the editing context again and
confirm the new plan. Keep returned IDs, read current items before deciding
recovery, and never retry creation or changes automatically; Pinterest has no
idempotency guarantee. After an uncertain creation, list the account's
campaigns or the campaign's ad groups and look for the name before anything
else. Every write spends several of the app's shared daily requests; do not
probe with speculative changes.
