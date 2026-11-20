# Snapchat Ads

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_snapchat_ads_readiness` to find its
Snapchat Ads connections. Show account names as numbered choices if more than
one exists; reuse the selected `connection_id` and `org_brand_id` for every
subsequent call. Never guess accounts or switch brands on a permission failure.
Direct missing or revoked access to the brand's Snapchat Ads integration; do not
request credentials.

Readiness reads the saved ad account and checks the connecting Snapchat user's
current role. If that role was removed, or Snapchat refused the saved
authorization, readiness says so in `next_step` instead of failing: relay it and
point the customer to the organization's Snapchat admin or to Reconnect. A
read-only connection cannot be elevated by asking; reconnecting with management
access is a Console step. `write_access_checked` is always false: readiness does
not test changes. When `is_test_account` is true, say that the account can never
serve live ads.

Reads change nothing. Quick Campaign and changes use the separate workflows
below, only on a manage connection with `management_permission_granted=true`
and only after the customer approves the exact plan. Never route Snapchat
requests through Meta, Google, Reddit or ChatGPT tools. Video, story and
collection ads, targeting beyond countries, other objectives and deletion are
not available here: point to Snapchat Ads Manager.

## Inventory

Snapchat calls ad groups "ad squads" and Ads Manager shows them as "Ad Sets".
Say "ad group" and mention the Snapchat name once if the customer uses it. Use
`list_snapchat_campaigns` / `get_snapchat_campaign`, then
`list_snapchat_ad_groups` / `get_snapchat_ad_group`, then `list_snapchat_ads` /
`get_snapchat_ad`. Use the campaign or ad-group filter when known. Show names
and statuses in short numbered lists, keeping the mapping stable across
follow-ups. IDs stay internal unless requested. Follow `next_cursor` with
unchanged connection, filters and page size; a page is not the complete
inventory, and an empty page does not prove there are no other pages. A positive
`skipped_items` means Snapchat returned rows that could not be read: say the
list is incomplete.

Budgets, bids and spend caps are Snapchat micro-currency amounts in the account
currency (1,000,000 per unit): show `daily_budget_micro` 50000000 USD as $50.00.
`status` (ACTIVE or PAUSED) is what the account set. `delivery_status` explains
whether Snapchat can deliver, for example `INVALID_NOT_EFFECTIVE_ACTIVE` (a
paused or invalid campaign or ad group above blocks it),
`INVALID_CAMPAIGN_HAS_NO_ACTIVE_AD_SQUAD` or `INVALID_AD_SQUAD_HAS_NO_ACTIVE_ADS`;
translate these into plain words and name the blocking campaign or ad group.
Snapchat adds values beyond its documented list, so describe an unfamiliar value
as Snapchat's own reason. An ad's `review_status` and `review_status_reasons`
explain ad review. Ad groups carry configured targeting and placement; ads carry
the creative ID but not creative content.

## Spend and results

Use `get_snapchat_performance` with explicit account-local `start_date` and
`end_date_exclusive`: `granularity=total` for 1–90 days or `daily` for 1–31 days.
Choose the level:

- `account`: account totals. Spend comes from the account itself; other metrics
  add up its campaigns, and `uniques` and `frequency` stay empty because they
  cannot be added. If campaign rows do not account for all spend, the other
  metrics are unknown and a warning names the uncovered spend.
- `campaign`: every campaign, or up to 10 `entity_ids`.
- `ad_group` or `ad`: up to 10 `entity_ids`, or one `campaign_id` to list that
  campaign's ad groups or ads.

Follow `next_cursor` before quoting totals. A daily page holds at most 620 rows;
use fewer days or a smaller `limit` if asked. If Snapchat says the report is too
large, narrow it the same way rather than retrying.

Metrics are impressions, swipes, spend, video views, uniques, frequency,
landing-page views, purchases and purchase value. `spend` and
`conversion_purchases_value` are already in the account currency
(`currency_code`); the `_micro` fields keep the raw amount. Purchases are
Snapchat-attributed Pixel events using 28-day swipe and 1-day view attribution
by conversion time; they are not store orders, and purchase value is not store
revenue. `missing_metrics` lists metrics Snapchat did not return; they are
unknown, not zero. Snapchat finalizes metrics 48 hours after the account-local
day: label results after `finalized_through` (and conversions after
`conversions_processed_through`) as provisional. When the dates include today,
`data_through` says where the totals stop; call that day partial. Never sum
`uniques` or `frequency` across rows or days.

## Boundaries and recovery

If completed-window totals stop before the requested end, report that coverage
is incomplete and retry later when Snapchat catches up. Do not present those
totals as complete or change the requested dates automatically.

Readiness verifies account access and the role only, not Snap Pixel
measurement, launch readiness or observed purchases. If event evidence is
insufficient, say so and recommend Pixel setup in Snapchat Ads Manager.

On a rate-limit error, wait a minute before retrying or narrow the request; never
retry in a loop. If a read fails after account access changed, direct the
customer to Reconnect on the Snapchat Ads integration card. Never present a
partial page as the whole account, invent totals, or quote raw provider codes.

## Create paused campaigns and ad groups

1. Resolve the brand and connection with `check_snapchat_ads_readiness`; it must
   show a manage connection with `management_permission_granted`. Read-only
   connections cannot be elevated by asking; reconnecting with management access
   happens in Console.
2. Collect the campaign name, a future start time, optional end time and optional
   campaign caps (daily and lifetime, each at least 20 units of the account
   currency). Campaigns are website traffic (Snapchat's TRAFFIC objective). For
   each ad group collect the name, goal (swipes or landing-page views), bid
   strategy (auto bid, or a maximum or target cost with a bid), a daily budget
   of at least 5 units or a lifetime budget with an end time, countries and,
   for several countries, one language, plus optional future dates inside
   the campaign's. Amounts are micro-currency (1,000,000 per unit); show readable
   amounts and say what you will send.
3. Present one compact plan: campaign name, dates and caps, then each ad group
   with goal, bidding, budget, countries, language and dates. Say that placement
   is automatic and that Snapchat's interest and custom-audience auto-expansion
   is on by default, so delivery can reach beyond the listed targeting. Say:
   "All new items will be paused. Activation requires separate approval."
   Obtain approval of that exact plan before any creation.
4. Call `create_snapchat_campaign`. Pass the returned `item` (or a fresh
   `get_snapchat_campaign` item) unchanged as `campaign` to
   `create_snapchat_ad_group`; the campaign must still be paused. New ad groups
   have no ads, so they cannot serve until the next section adds them. Relay
   any Snapchat warnings in the result.

## Quick campaign and new ads

1. For Quick Campaign, resolve one product with `list_brand_products` and
   explain that `prepare_snapchat_campaign` writes three Snap Ad variants
   (headline of at most 34 characters and a Shop Now or More button) from saved
   brand knowledge and costs 10 Mighty credits when billing is enabled;
   preparing again is another paid generation. Snap Ads have no body text.
2. Every Snapchat ad runs as a Public Profile, the brand's page on Snapchat.
   Preparation returns the profiles found on the account's existing ads in
   `profile_ids`; ask which one when there is more than one. When it says none
   is known, ask the customer for the Public Profile ID shown in Snapchat
   Business Manager under Public Profiles and pass it as `profile_id`; nothing
   is charged until a profile is known. Never invent a profile ID.
3. Present one plan: the campaign and ad group from the section above, then
   each ad with its name, headline, button, Public Profile, the product image
   and the destination. Say that the image is shown full screen, scaled and
   padded to Snapchat's portrait format, and: "All new items will be paused.
   Activation requires separate approval."
4. After approval, create the campaign and ad group as above, then call
   `create_snapchat_ad` for each approved ad with the ad group `item` from the
   creation result or `get_snapchat_ad_group`, unchanged. Snapchat reviews each
   ad before it can run.
5. Keep every returned ID and `recovery_receipt`. Recovery passes the receipt
   and the returned `creative_id` or `media_id` with the same ad group and
   image URL. While only the image exists, a refused creative can be retried
   with a corrected name, headline, button, Public Profile or destination after
   the customer approves the change; once a creative exists, all of them must
   stay the same. Bare IDs are refused. Receipts expire after 24 hours and
   retries do not extend that expiry. A refused image needs another image and
   a new create without the receipt.
   If an ad submission is uncertain, list the ad group's ads and look for the
   name before any retry; a receipt does not prevent duplicate ads. If media
   creation is uncertain without an ID, reconcile the image library first.

## Change settings and status

1. Read `get_snapchat_edit_context` for the target campaign, ad group or ad and
   pass its `account` and `item` unchanged; do not edit or rebuild the item.
   Each change asserts the item's current values for the settings it changes,
   so another edit to those settings makes Snapchat refuse it without applying
   anything, while unrelated edits do not block it.
2. Present a before/after plan naming the affected item, readable amounts in
   the account currency and the delivery impact, and get approval of that exact
   plan.
3. Use `update_snapchat_campaign` for a campaign's name, daily or lifetime cap,
   start or end time, or to remove the end time or a cap. The daily cap must be
   at least a quarter of its ad groups' combined daily budgets, and a lower
   lifetime cap at least 1.1 times what was already spent. Use
   `update_snapchat_ad_group` for an ad group's name, its existing daily or
   lifetime budget, bid strategy and bid, or dates; switching to auto bid
   removes the bid. New start times must be in the future and ad-group dates
   must stay inside the campaign's.
4. Use `set_snapchat_status` only after explicit approval of the exact target
   and the desired ACTIVE or PAUSED state. Activation may start real spend and
   changes only the selected item: activating a campaign does not activate its
   ad groups or ads, and the result names paused campaigns and ad groups that
   still block delivery. To stop delivery, pause the campaign first.

Results report `verified`, `unchanged`, `rejected` (Snapchat refused, so nothing
was applied), `confirmation_pending` (accepted but not yet confirmed) or
`uncertain` (the submission may or may not have applied). When Snapchat refused
because the settings changed first, read the editing context again and confirm
the new plan. Keep returned IDs, read current items before deciding recovery,
and never retry creation or changes automatically; Snapchat has no idempotency
guarantee. After an uncertain creation, list the account's campaigns or the
campaign's ad groups and look for the name before anything else.
