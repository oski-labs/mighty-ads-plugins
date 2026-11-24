# TikTok Ads

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_tiktok_ads_readiness` to find its TikTok
connections. Show advertiser account names as numbered choices if more than one
exists; reuse the selected `connection_id` and `org_brand_id` for every
subsequent call. Never guess accounts or switch brands on a permission failure.
Direct missing or revoked access to the brand's TikTok integration; do not
request credentials. Readiness confirms the advertiser is still authorized; it
does not verify the Pixel, Events or launch readiness.

TikTok changes need a connection saved with management access; a read-only
connection cannot be elevated by a request. Supported changes are creating a
paused Traffic campaign, a paused ad group in it and a paused Spark Ad from an
existing library video or TikTok post; campaign and ad group budget amounts; and
enabling or disabling one campaign, ad group or ad. Other objectives, editing
targeting or bids, uploading videos, image or carousel ads, custom identities,
creating identities and deletion are unavailable; explain that and perform no
substitute change.

## Inventory

Use `list_tiktok_campaigns` / `get_tiktok_campaign`, then `list_tiktok_ad_groups`
/ `get_tiktok_ad_group`, then `list_tiktok_ads` / `get_tiktok_ad`. Use campaign
and ad group filters when known. Show names and customer-facing statuses in
short numbered lists, keeping the mapping stable across follow-ups. IDs stay
internal unless requested. Follow `next_cursor` with unchanged connection,
filters and page size; a page is not the complete inventory, and a skipped-row
warning means the list is incomplete. Stop on an error rather than invent totals.

Statuses have two parts. `operation_status` is the configured switch (ENABLE,
DISABLE or FROZEN). `secondary_status` is TikTok's delivery state, such as
`CAMPAIGN_STATUS_BUDGET_EXCEED` or `ADGROUP_STATUS_CAMPAIGN_DISABLE`; it is not
returned in the sandbox. Explain a paused or budget-exceeded campaign as the
blocker for its ad groups and ads by name. A status alone is not proof that an
ad delivered; check dated spend and impressions.

Budgets can belong to the campaign (`budget_optimize_on` true, ad group budget
`0.0`) or to each ad group. Inspect both before explaining spending controls.
Budgets and bids are in the advertiser's account currency units as TikTok
returns them, not micros or minor units. A `scheduled_budget` takes effect at
midnight in the account time zone. Schedules and create/modify times are UTC.
Ad group targeting (locations, ages, gender, languages, placements) describes
intended audiences; performance describes reported delivery. Ad creative fields
cover configured text, call to action, identity, video or image references and
destination; Spark Ads reference a TikTok post (`tiktok_item_id`) instead of an
uploaded video.

## Spend and results

Use `list_tiktok_performance` with explicit account-local `start_date` and
`end_date_exclusive`, a level (advertiser, campaign, ad group or ad) and the
selected campaign, ad group or ad filters. Totals cover up to 365 days;
`granularity=daily` covers up to 30 days. Choose one `metric_group`:

| Group      | Evidence                                                                                         |
| ---------- | ------------------------------------------------------------------------------------------------ |
| `delivery` | Spend, impressions, clicks, CTR, CPC, CPM, conversions, results and their costs, reach, frequency |
| `video`    | Video plays, 2-second and 6-second views, 25/50/75/100% completions, average play, engaged views  |
| `website`  | Pixel purchases (`complete_payment`), purchase value, ROAS, add to cart, checkout, page views      |
| `shop`     | TikTok Shop purchases, purchase value and ROAS                                                    |

Set `country_breakdown=true` for rows per country; reach and frequency are not
reported per country. Follow every page needed for the requested scope and label
partial results. Present money with the returned account currency and readable
rates. CTR and conversion rate are already percentages; do not multiply by 100.
`total_complete_payment_rate` is total purchase value despite its name. Do not
sum reach across campaigns, days or countries, or average CPC, CTR or ROAS;
request the level total for a deduplicated figure.

Results are TikTok-attributed events under each ad group's click and view
attribution windows. Most metrics settle within about 30 minutes and reach within
about 16 hours; recent days can change. Missing metrics are unknown, not zero.
TikTok-attributed purchases and store orders are separate measures. Name the
largest supported gap, the evidence and a concrete next check; do not invent a
cause, guaranteed savings or a processing-time promise.

## Boundaries and recovery

- A reconnect prompt means TikTok rejected the token or the advertiser is no
  longer authorized; send the customer to the brand's TikTok integration.
- A rate-limit message means wait a few minutes; do not retry in a loop.
- "Nothing was sent" means TikTok could not be reached before the change went
  out; the item is unchanged and the change can be offered again later.
- A continuation error means the brand, connection, filters or page size
  changed; restart the list with the same arguments.
- `write_state` on a detail read binds a later change to what was read; it is
  not a permission or an approval.

## Create a paused campaign

1. Resolve the brand and management connection, then confirm the plan with the
   customer: campaign name, daily, lifetime or unlimited budget in the account
   currency, and whether TikTok should optimize the budget across ad groups.
   An optimized campaign uses a lifetime or dynamic daily budget (an average
   daily amount that may run up to 125% on a single day).
   Say: "The campaign will be created paused with no ad groups or ads; activation
   requires separate approval." Only the Traffic objective is available.
2. Call `create_tiktok_campaign` once with the approved plan, passing a stable
   `idempotency_key` for that plan so an accidental repeat within ten seconds
   creates no duplicate. `verified` returns
   the new campaign ID. `confirmation_pending` means TikTok created it but the
   settings could not be confirmed: read the campaign before continuing. When
   the message lists settings that differ from the plan, show them to the
   customer; if it says TikTok reports the item enabled, offer to disable it
   before anything else.
   `uncertain` means it may or may not exist: list the campaigns, following
   every page, and look for its name before creating again. Never resubmit
   automatically.
3. Continue with a paused ad group in the new campaign when the customer wants
   one.

## Create a paused ad group

1. Read the campaign with `get_tiktok_campaign` and keep its `write_state`.
   Only Traffic campaigns can take new ad groups.
2. Confirm the plan: ad group name, countries (two-letter codes such as `US`),
   adult age groups (all 18+ by default) and gender, and the budget. If the
   campaign uses budget optimization it owns the budget, so no ad group budget is
   set; otherwise choose a daily budget or a lifetime budget with an end date (a
   daily campaign allows only daily ad groups; TikTok's minimum is about 20 USD a
   day in the account currency). Say: "It promotes your website, optimizes for
   clicks at the lowest cost with automatic placement, and is created paused with
   no ads; activation requires separate approval."
3. Call `create_tiktok_ad_group` once with the approved plan, the campaign's
   `write_state` as `expected_campaign_state` and a stable `idempotency_key`. A
   country TikTok does not offer this advertiser is refused before anything is
   sent; tell the customer which. `uncertain` means it may exist: list the
   campaign's ad groups before creating again.

## Create a paused ad

Ads on TikTok run under a TikTok account (a Spark Ad); custom identities cannot
be used. An ad either runs a video from the ad account's library under that
account, or promotes one of the account's existing public posts.

1. Read the ad group with `get_tiktok_ad_group` and keep its `write_state`.
2. Call `list_tiktok_creation_assets` with `asset=identities`. Offer only
   available accounts: `can_push_video` for library videos, `can_pull_video` for
   existing posts. If none exist, the customer must link a TikTok account to the
   ad account in TikTok Ads Manager first; say so and stop.
3. For a library video, list `asset=videos` (optionally by name) and let the
   customer choose. For an existing post, list `asset=posts` for the chosen
   identity and choose a public post.
4. Confirm the plan: ad name, the TikTok account, the video or post, the caption
   (required for a library video, up to 100 characters, no emoji), the call to
   action and the `https` landing page. An existing post keeps its organic
   caption; do not offer caption edits, and omit `ad_text` when promoting it.
   For a library video say that its cover is
   added to the ad account's image library as the ad cover. Say: "The ad is
   created paused; TikTok reviews it, and activation requires separate approval."
5. Call `create_tiktok_ad` once with the approved plan and the ad group's
   `write_state` as `expected_adgroup_state`; if the ad group changed since that
   read, read it again and confirm the plan. There is no duplicate protection for
   ads: after `uncertain`, list the ad group's ads before creating again.
   If the result says no ad creation was attempted because the cover upload is
   unresolved, reconcile the image library first. Another call uploads a new
   cover; this tool cannot reuse a cover ID.

## Change budgets and statuses

1. Read the target with `get_tiktok_campaign`, `get_tiktok_ad_group` or
   `get_tiktok_ad` and keep its `write_state`. Present a compact before/after
   plan naming the item, the budget owner and mode, the amount in the account
   currency and the delivery impact, and obtain approval of that exact plan.
2. `update_tiktok_campaign_budget` changes the amount under the existing daily
   or lifetime mode; TikTok rejects amounts below 105% of current spend. A
   campaign without its own budget must be changed in Ads Manager.
3. `update_tiktok_ad_group_budget` applies a lifetime budget immediately and
   schedules a daily budget for midnight in the account time zone; tell the
   customer the returned `effective_at` date and that today's budget is
   unchanged. TikTok refuses budget changes between 23:55 and 00:00 account time.
   An ad group whose campaign owns the budget is rejected.
4. `set_tiktok_status` enables or disables only the selected item. Enabling may
   start spend. It never enables other levels; name the disabled campaign or ad
   group from the warnings as blockers and ask before changing them. Terminated
   items cannot be enabled. To stop delivery, disable the campaign first.

Report `verified` as confirmed, `unchanged` as already matching, `rejected` as
not applied (TikTok refused it, including rate limits and concurrent-change
conflicts), and `uncertain` or `confirmation_pending` as unresolved: read the
current settings before considering another change. Keep any returned ID. Never
retry automatically after a timeout or a readback mismatch, and never delete.
