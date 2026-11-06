# Reddit Ads

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_reddit_ads_readiness` to find its Reddit
Ads connections. Show account names as numbered choices if more than one exists;
reuse the selected `connection_id` and `org_brand_id` for every subsequent call.
Never guess accounts or switch brands on a permission failure. Direct missing or
revoked access to the brand's Reddit Ads integration; do not request credentials.
Readiness confirms the saved ad account with a live identity read and reports
whether the connection holds management permission. A read-only connection
cannot be elevated by asking; reconnecting with management access is a Console
step. Readiness also names Reddit's account approval state when it is not
valid, because an unapproved account blocks delivery even though reads work.

Reddit inventory and performance tools are read-only. Paused campaign and
ad-group creation, budget edits and pause/activation use the separate guarded
workflow below; never route Reddit changes through Meta, Google or ChatGPT write
tools, and never create ads, posts or audiences here.

## Inventory

Use `list_reddit_campaigns` / `get_reddit_campaign`, then
`list_reddit_ad_groups` / `get_reddit_ad_group`, then `list_reddit_ads` /
`get_reddit_ad`. Use the campaign or ad-group filter when known. Show names and
customer-facing statuses in short numbered lists, keeping the mapping stable
across follow-ups. IDs stay internal unless requested. Follow `next_cursor` with
unchanged connection, filters and page size; a page is not the complete
inventory, and an empty page does not prove there are no other pages. Lists omit
deleted items; details can still return them.

Budgets, bids and spend caps are Reddit microcurrency amounts in the account
currency (1,000,000 per unit): show `goal_value_micros` 50000000 USD as $50.00.
A campaign with `is_campaign_budget_optimization` owns the budget through its
`goal_type` and `goal_value_micros`; otherwise each ad group owns its own goal.
`configured_status` is what the account set. `effective_status` and
`delivery_status` explain why an item is not delivering, for example
`CAMPAIGN_PAUSED`, `PENDING_APPROVAL`, `PENDING_BILLING_INFO` or `REJECTED`;
an ad's `rejection_reason` names Reddit's policy reason. Ad groups carry the
configured `targeting` (geolocations, communities, interests, keywords,
devices); ads carry the post link and click URL but not the post text or media.
A Reddit Max campaign (`is_max`) is managed by Reddit; describe it as such.

## Spend and results

Use `get_reddit_performance` with explicit account-local `start_date` and
`end_date_exclusive` (1–366 days), a `level` of account, campaign, ad_group or
ad, and up to 20 `entity_ids` from the inventory tools; without IDs every item
at that level is reported. Use `granularity=daily` for trends and comparable
total windows for a decline. Follow `next_cursor` before quoting totals.

Metric groups: `delivery` (impressions, clicks, spend, CTR, CPC, eCPM and
engaged clicks), `reach` (deduplicated reach and frequency),
`video` (starts, quartiles, viewability and rates) and `conversions` (Reddit
Pixel key conversions, purchases with value and items, sign-ups, page visits,
add-to-carts and leads). Spend, CPC, eCPM, cost per key conversion and purchase
value are already converted into the account currency; `spend_micros` keeps the
raw amount. `ctr` and rates are Reddit's values as returned. Metrics can take up
to six hours to stabilise and late conversions change earlier days during
Reddit's daily refresh, so mark today and yesterday as provisional.

`missing_metrics` lists requested metrics Reddit did not return; they are
unknown, not zero. Conversions are Reddit-attributed Pixel events under the
account's attribution window; click and view counts are attribution types, not
orders, and purchase value is not store revenue. Rows cover only the listed
entities; account level is the only deduplicated account total, and `reach`
must never be summed across rows or days.

Pass `breakdown` to the same tool for one dimension per call: country, region,
placement, os_type, gender, community, interest or keyword. Each row's
`dimension` is partial by that value and is not a total. Community, interest and
keyword breakdowns cannot be combined with each other or with geography; run
separate reads and label each.

## Boundaries and recovery

Readiness verifies account access only, not Pixel measurement, launch readiness
or observed purchases. If event evidence is insufficient, say so and recommend
Pixel and conversion setup in Reddit Ads Manager.

On a rate-limit error, wait the reported time before retrying or narrow the
request; never retry in a loop. If a read fails after account access changed,
direct the customer to Reconnect on the Reddit Ads integration card. Never
present a partial page as the whole account, invent totals, or quote raw
provider codes.

## Create paused campaigns and ad groups

1. Resolve the brand and connection with `check_reddit_ads_readiness`; it must
   show a manage connection with `management_permission_granted`. Read-only
   connections cannot be elevated by asking; reconnecting with management access
   happens in Console.
2. Collect the campaign name, objective and, when the customer wants one budget
   for the whole campaign, campaign budget optimization with a daily or lifetime
   goal, bid strategy and type, Pixel, a start time and, for a lifetime goal,
   an end time. Otherwise each ad group carries its own goal, bid and schedule,
   and the campaign takes no start time. Amounts are microcurrency (1,000,000 per unit); show
   readable amounts and say what you will send.
3. Present one compact plan: campaign name, objective, budget owner and amount,
   then any ad groups with goal, bidding, Pixel, countries and schedule. Say:
   "All new items will be paused. Activation requires separate approval."
   Obtain approval of that exact plan before any creation.
4. Call `create_reddit_campaign`. Then read `get_reddit_campaign` and pass its
   fresh `item.write_state` into `create_reddit_ad_group`. New ad groups have no
   ads, so they cannot serve; explain that ads and posts are added in Reddit
   Ads Manager for now.

## Change budgets and status

1. Read `get_reddit_edit_context` for the target campaign, ad group or ad and
   reuse its `account` and `write_state` as returned. Inventory `item.write_state`
   is for creation parents and cannot replace the editing context. When
   `campaign.is_max` is true, Reddit manages the campaign: do not plan changes
   to it, its ad groups or ads, or new ad groups under it.
2. Present a before/after plan naming the affected item, the account currency
   and delivery impact, and get approval of that exact plan. Expected state
   detects stale settings; it is not proof of approval.
3. Use `update_reddit_budget` for an ad group's goal value, or for a campaign's
   goal value and spend cap when the campaign owns the budget. The tool refuses
   the wrong budget owner; objective, bidding, targeting and names are not
   editable here.
4. Use `set_reddit_status` only after explicit approval of the exact target and
   the desired ACTIVE or PAUSED state. Activation may start real spend and
   changes only the selected item: a paused campaign or ad group still blocks
   the items beneath it, and the result names what remains paused. To stop
   delivery, pause the campaign first.

Results report `verified`, `unchanged`, `rejected` (nothing applied; the
message names the fields Reddit flagged), `confirmation_pending` (accepted but
not yet confirmed) or `uncertain` (the submission may or may not have applied). Keep returned IDs, read current
items before deciding recovery, and never retry creation or updates
automatically; Reddit has no idempotency guarantee.
