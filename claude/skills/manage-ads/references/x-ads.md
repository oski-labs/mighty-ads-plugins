# X Ads

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_x_ads_readiness` to find its X Ads
connections. Show account names as numbered choices if more than one exists;
reuse the selected `connection_id` and `org_brand_id` for every subsequent call.
Never guess accounts or switch brands on a permission failure. Direct missing or
revoked access to the brand's X Ads integration; do not request credentials.
Readiness reports the authorizing X user's role on the account. A read-only
connection or a Campaign analyst role cannot be elevated by asking.

X inventory and performance tools are read-only. Quick Campaign, paused
campaign and ad-group creation, new promoted-only posts with website cards,
adding posts as ads, location targeting, supported edits and pause/activation
use the separate guarded workflow below. Anything else on X (video or carousel
posts, other targeting, audiences, deletion) is not available here: say so when
asked and point to X Ads Manager, and never route X changes through Meta, Google
or ChatGPT write tools.

## Inventory

Use `list_x_campaigns` / `get_x_campaign`, then `list_x_ad_groups` /
`get_x_ad_group`, then `list_x_ads` / `get_x_ad`. X calls ad groups "line items"
and ads "promoted posts"; use campaign, ad group and ad with customers. Use the
campaign or ad-group filter when known. Show names and customer-facing statuses
in short numbered lists, keeping the mapping stable across follow-ups. IDs stay
internal unless requested. Follow `next_cursor` with unchanged connection,
filters and page size; a page is not the complete inventory, and an empty page
does not prove there are no other pages.

Budgets, bids and funding-instrument credit figures are X micro amounts in
the funding currency (1,000,000 per unit): show 10000000 USD as $10.00.
`entity_status` is the configured state. Only campaigns carry a `servable`
flag and `reasons_not_servable` (for example `PAUSED_BY_ADVERTISER`,
`INCOMPLETE`) explaining why they are not delivering; ad groups and ads report
no delivery state, an ad group needs targeting and at least one ad to serve,
and those details are not included. Ad text is the promoted post's text when X returns it;
a missing text is unknown, not blank. `approval_status` is X's review state.
Use `list_x_funding_instruments` when the customer asks what pays for campaigns
or why nothing delivers: `able_to_fund=false` blocks every campaign under it.
X also reports its placeholder for an account with no card as able to fund, and
its API can keep showing that placeholder after a card is added. When a result
flags a zero credit limit, ask the customer to check Billing in X Ads Manager
before expecting delivery; do not tell them they have no card.

## Spend and results

Use `list_x_performance` with explicit account-local `start_date` and
`end_date_exclusive` (1–7 days), a `level` of account, campaign, ad_group or ad,
and up to 20 `entity_ids` from the inventory tools; IDs outside the account
are refused. When `entity_ids` is omitted the first 20 items at that level are
used and the result says so; pass IDs for others. Use `granularity=daily` for
trends and comparable total windows
for a decline. Windows longer than 7 days are not available yet; explain the
limit rather than stitching many windows together silently, or run separate
windows and label each. A 7-day window that crosses a daylight-saving change
is refused as one day too long, a daily breakdown cannot cross such a change
(split it there or use a total), and accounts in a time zone with a partial-hour
offset (for example UTC+5:30) cannot be reported by account-local day yet.

Metric groups: `engagement` (impressions, engagements, clicks, url_clicks,
likes, replies, retweets, follows, card engagements), `billing`
(billed engagements and spend), `video` (views and completion milestones) and
`web_conversion` (X pixel website events). Request `billing` whenever money is
discussed: `spend` is `billed_charge_local_micro` converted to the funding
currency shown as `currency_code`. Spend is generally final after about 3 days
and billing can adjust for up to 14 days; other metrics lock after 24 hours.
Mark today as partial.

`conversions` keeps X's web-conversion objects by event type, each with
post-view, post-engagement and assisted counts plus order quantity and sale
amount for the bucket. Do not add post-view and post-engagement counts to a
grand total without saying they are attribution types, and do not treat
`sale_amount` as store revenue. X reports metrics with no activity as null,
which the tools show as 0; `missing_metrics` lists requested metrics X did not
return at all, and those are unknown, not zero. Clicks and `url_clicks` differ: use
`url_clicks` for link traffic. Rows cover only the listed entities; account
level is the only deduplicated account total.

## Boundaries and recovery

Readiness verifies account access and role only, not pixel measurement, launch
readiness or observed purchases. If event evidence is insufficient, say so and
recommend the X pixel and conversion setup in X Ads Manager.

On a rate-limit error, wait before retrying or narrow the request; never retry
in a loop. If a read fails after account access changed, direct the customer to
Reconnect on the X Ads integration card. Never present a partial page as the
whole account, invent totals, or quote raw provider codes.

## Quick campaign

1. Resolve the brand and a manage connection with `check_x_ads_readiness`, and
   one product with `list_brand_products`. Explain that `prepare_x_campaign`
   writes three promoted-only post variants from saved brand knowledge and costs
   10 Mighty credits when billing is enabled; preparing again is another paid
   generation. It first checks that the connected X user can publish ads posts
   for the account and explains the X Ads Manager role to grant when not.
2. Present one plan: campaign and ad-group names, the posts to publish (text,
   card title, the product image and destination), the funding instrument, daily
   budget, goal, AUTO bidding unless the customer wants a maximum bid, the
   account-local start and end, and the locations. Say the image is
   center-cropped to a square when it does not fit X's card. Say: "All new items
   will be paused. Activation requires separate approval." Explain that X keeps
   each published post (promoted-only, never on the profile) even if it is not
   used, because X cannot delete it.
3. After approval of that exact plan, call `create_x_campaign`, then
   `create_x_ad_group` with the campaign's fresh `item.write_state`,
   `set_x_ad_group_locations`, then for each approved post `create_x_post`
   followed by `add_x_ad` with the returned `tweet_id` and a fresh edit
   context. Inspect each result before the next step; stop on anything not
   `verified` and report what exists.
4. If `create_x_post` is `uncertain`, check `list_x_posts` for a post with the
   planned name before any retry. A failure before the post says no post was
   published and is safe to retry once the cause is fixed.

## Create paused campaigns and ad groups

1. Resolve the brand and connection with `check_x_ads_readiness`; it must show a
   manage connection with `management_permission_granted`. Read-only
   connections or a Campaign analyst role cannot be elevated by asking.
2. Use `list_x_funding_instruments` and present the fundable instruments by
   name/currency when more than one exists. Collect the campaign name. New
   campaigns keep budgets on each ad group, as in X Ads Manager: a daily budget
   is required and a total budget is optional. Budgets are funding-currency micros
   (1,000,000 per unit); show readable amounts and say what you will send.
3. Present one compact plan: campaign name, funding instrument, then any ad
   groups with daily budget, goal (link clicks or site visits), AUTO bidding or
   MAX with a bid and an account-local start and end (X requires both). Say: "All new
   items will be paused. Activation requires separate approval." Obtain approval
   of that exact plan before any creation.
4. Call `create_x_campaign`. Then read `get_x_campaign` with the same
   connection and pass its fresh `item.write_state` into `create_x_ad_group`.
   New ad groups have no targeting and no ads, so they cannot serve until the
   next section's steps add them.

## Add ads and locations

1. Use `list_x_posts` to show the brand's published posts by name and text, and
   `search_x_locations` to resolve each place the customer names; confirm the
   match when several places share a name. Link-click ad groups need a post
   with a website card or a link (`has_card` shows a card); X refuses others.
   To make a new post, use `create_x_post` after approval of its text, card
   title, image and destination.
2. Read `get_x_edit_context` for the ad group. It lists current locations.
   Present the post to add, or the current → new locations, and get approval
   of that exact plan.
3. Call `add_x_ad` with the post's `tweet_id`, or `set_x_ad_group_locations`
   with every location the ad group should target; it replaces existing
   locations and leaves other targeting, including excluded locations, alone. Read the context again before a
   second change, since the first one changes the ad group's `write_state`.
4. X creates ads active and reviews them. Before activation, check each ad's
   `approval_status` with `list_x_ads`; a rejected ad will not deliver.

## Edit existing settings and change status

1. Read `get_x_edit_context` for the target campaign or ad group and reuse its
   `account` and `write_state` exactly. Inventory `item.write_state` is for
   creation parents and cannot replace the editing context.
2. Present a before/after plan naming the affected campaign or ad group, the
   funding currency and delivery impact, and get approval of that exact plan.
   Expected state detects stale settings; it is not proof of approval. A pause
   is not blocked by settings changed since the read.
3. Use `update_x_campaign` for name, daily or total budget. Use
   `update_x_ad_group` for name, bid strategy and bid, schedule or budgets.
   Campaigns Mighty creates keep budgets only on their ad groups, so change
   those ad groups' budgets; a campaign budget is refused there. A campaign whose `budget_optimization` is `CAMPAIGN` keeps its budget on the
   campaign: X refuses ad-group budgets and any move, and X Ads Manager cannot
   save its ad groups. Change its budget with `update_x_campaign`. Omit
   unchanged fields; do not use null. Objective, placements and goal cannot be
   edited here, and ads cannot be edited, only added.
4. Use `set_x_status` only after explicit approval of the exact target and the
   desired ACTIVE or PAUSED state. Activation may start real spend and changes
   only the selected item: a paused campaign still blocks its ad groups, and the
   result counts ad groups that remain paused or have no daily budget, naming
   the first five, and warns when the item's end time has passed. Summarize
   those counts and offer to list the rest with `list_x_ad_groups`. To stop delivery, pause the
   campaign first. If the editing context lists `incomplete_checks`, tell the
   customer which delivery checks could not run before asking to activate.
   If it lists `activation_blockers` (a campaign without ad groups, an ad group
   without ads), activation is refused: guide the customer through the missing
   setup first instead of asking to activate.

Results report `verified`, `unchanged`, `rejected` (nothing applied, including
rate limits, a refused authorization and items or access that disappeared; when
X refuses a setting, `provider_error_code` and `provider_error_attribute` name
it for recovery, but tell the customer only the plain message), `confirmation_pending`
(accepted but not yet confirmed) or `uncertain` (X failed or did not answer in
time, so the change may or may not have applied); `applied` echoes what was
sent. Keep returned IDs, read current items before deciding recovery, and never
retry creation or updates automatically; X has no idempotency guarantee.
