# Google Ads: inspect campaigns and spend

Answer Google Ads inspections without change approval. Search creation, supported
budget/bid changes, supported edits and enable/pause requests follow the confirmed plan below.
Other campaign types and unsupported edits remain inspection-only. Never
substitute ChatGPT tools or imply an unconfirmed change was made.

## Find the right account and items

Reuse the selected connection and discovered `org_brand_id`. Use
`check_google_ads_readiness` when account identity, currency or timezone is needed.
It checks account read access, not launch readiness, measurement or write access.

| Question                                                               | Tools                                                                        |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| Campaigns and settings                                                 | `list_google_campaigns`, `get_google_campaign`                               |
| Ad groups and bids                                                     | `list_google_ad_groups`, `get_google_ad_group`                               |
| Ads, destinations and review                                           | `list_google_ads`, `get_google_ad`                                           |
| Spend and performance                                                  | `list_google_performance`                                                    |
| Configured keywords                                                    | `list_google_keywords`                                                       |
| Searches that triggered ads                                            | `list_google_search_terms`                                                   |
| Campaign targeting and exclusions                                      | `list_google_campaign_criteria`                                              |
| Shared negative lists and their keywords                               | `list_google_campaign_criteria` with `view=shared_lists` or `view=shared_list_keywords` |
| Assets attached directly to a campaign                                 | `list_google_campaign_assets`                                                |
| Conversion settings and goals                                          | `list_google_conversion_settings` with `kind=actions` or `kind=goals`        |
| Provider conversion counts                                             | `list_google_performance` for the selected campaign and dates                |
| Keyword, conversion-action, device, country or destination performance | `list_google_performance` with `breakdown`                                   |

Resolve campaign names in that brand's list; resolve groups and ads within the
selected campaign/group. Show short numbered choices with names and statuses;
use a headline or destination when an ad has no name. Keep numbers stable for
follow-up selections. Ask only when the channel, brand or target is ambiguous.
An enabled campaign/ad is not proof it is serving; review and delivery are separate.

Follow `next_cursor` with unchanged filters when needed to answer the question.
Label a partial list, never call its sum an account total. If a requested item is
missing, check subsequent pages before concluding it does not exist. If a list
changes or continuation expires, restart once; if it remains incomplete, explain
what could be checked and offer a narrower search. Do not make users handle cursors.

## Explain performance simply

Use the requested dates. If absent, use the last seven completed days in the
account's timezone and state the actual dates. Tools require `start_date` and
`end_date_exclusive` on every page; include the day after the user's last inclusive
date. Do not invent the timezone. Ask for dates if the intended period is unclear.

For `list_google_performance`, choose exactly one of `level` or `breakdown`:

- Use `level=campaign` for campaign totals, or `level=ad_group` or `level=ad`
  for those aggregates. Omit `breakdown`.
- Use `breakdown=keyword` for positive keyword performance, or the supported
  `conversion_action`, `device`, `location` or `landing_page` breakdown. Omit
  `level`; breakdown reports allow a campaign filter, not ad-group or ad filters.

Never omit both selectors or send both. Keep the selector, dates and filters
unchanged on every page. A selector validation error is an invalid request, not
evidence of a disconnected Google account or zero activity; correct the request
before interpreting the report.

Convert cost, budget and CPC micros by dividing by 1,000,000; show the account
currency. Convert CTR ratios to percentages. Conversion value is already in
currency, not micros; keep fractional conversions. Show budget period and whether
it is shared. Configured bids are not actual average CPC. For example,
12,500,000 cost micros and 0.025 CTR become $12.50 USD and 2.5%, in a USD account.

Lead with the requested answer and a few relevant metrics, not every field.
Aggregate only a complete, identically scoped report; recompute CTR/CPC from
totals rather than averaging row rates. Empty results do not establish zero
activity, and unavailable metrics are not zero. Recent conversion figures may
change; reported conversions/value are not necessarily orders or revenue. Do not
compare channel ROAS as equivalent without checking attribution and definitions.

## Limits and recovery

Explain limitations when they affect the answer, not as a boilerplate warning list.
Responsive search ads include copy; other formats may return only identity,
status and destinations. Missing copy does not mean the ad is empty. Configured
keywords differ from observed search terms; term reports cover Search campaigns
and omit some searches for privacy. Keyword inventory includes ad-group negative
keywords, but excludes campaign/shared negative lists and Performance Max search
themes. Keyword performance excludes negative keywords. Use campaign criteria and
shared-list tools for campaign exclusions; these exclude account-level negative
lists. Campaign assets exclude account, ad-group and PMax asset-group
attachments. Conversion settings describe configuration; they do not verify
tracking health. Country performance separates presence from interest, rather
than showing city-level targeting. Use returned country names/codes, not criterion
IDs; missing labels are unknown, never guessed. Conversion-action breakdowns have no spend or
click metrics; null is unavailable, so do not compute per-action CPA or ROAS.

Translate errors into a next step: missing connection/access → connect or reconnect
Google Ads in the selected brand's Integrations; quota/temporary outage → try
later, not reconnect. Missing targets → refresh the campaign/group selection.
Never switch brands to bypass an error, expose credentials, or claim a failed
read means no campaigns or no spend. Finish with one useful next step.

## Performance Max inspection

Discover `channel_type=PERFORMANCE_MAX` in `list_google_campaigns`, then use
asset groups instead of Search ad groups. PMax creation, edits, pause and
activation are unavailable; never route these requests through a Search writer.

| Question | Tool |
| --- | --- |
| PMax bidding, merchant feed, budget and automation | `get_google_pmax_campaign` |
| Group URLs, configured/serving status and strength | `list_google_pmax_asset_groups` |
| Attached copy, images, YouTube assets, role and policy | `list_google_pmax_assets` |
| Signals, listing partitions, coverage, top combinations or generated URL assets | `list_google_pmax_configuration` with the corresponding `kind` |
| Spend, conversions and value | `list_google_pmax_performance` with `report=campaign` |
| Spend by Google network | `list_google_pmax_performance` with `report=channel` |
| Product/video usage by network | `list_google_pmax_performance` with `report=channel_usage` |
| Creative evidence | `list_google_pmax_performance` with `report=asset_group`, `asset` or `asset_channel` |
| Retail performance | `list_google_pmax_performance` with `report=product` or `product_group` |
| Group spend by network | `list_google_pmax_performance` with `report=asset_group_channel` |
| Product attributes, network or device | `list_google_pmax_performance` with `report=product_attributes`, `product_channel` or `product_device` |
| Sold products and attributed product profit | `list_google_pmax_performance` with `report=sold_product` |
| Shopping auction competition | `list_google_pmax_performance` with `report=shopping_competitive` |
| Linked feeds, sets, members and labels | `list_google_pmax_configuration` with `kind=asset_sets`, `asset_set_assets`, `page_feed_assets` or `campaign_labels` |
| Inherited account assets and sets | `list_google_pmax_configuration` with `kind=customer_assets` or `customer_asset_sets` |
| Existing simulations, experiments and adjustments | `list_google_pmax_configuration` with `kind=simulations`, `experiment_arms`, `seasonality_adjustments` or `data_exclusions` |
| Account recommendations and auto-apply settings | `list_google_pmax_configuration` with `kind=account_recommendations` or `recommendation_subscriptions` |
| Search evidence | `list_google_pmax_performance` with `report=search_term` or campaign-scoped `search_category` |
| Placement impressions | `list_google_pmax_performance` with `report=placement` |
| Device, conversion-action, targeted-location or destination evidence | `list_google_pmax_performance` with `report=device`, `conversion_action`, `location` or `landing_page` |

Use explicit complete account-local dates, at most 366 days for totals or 31 for
`granularity=daily`. Hourly campaign-resource reports cover at most seven days;
`day_of_week`, `weekly` and `monthly` are named calendar buckets. Placement reports
support total/daily only, and targeted-location reports exclude day-of-week.
Week/month buckets can be partial at the selected window boundaries.
Default to seven complete days. If the returned metrics are
zero, state zero for that interval and offer a longer interval; never silently
replace dates with a year. Follow pagination with unchanged filters. Inventory
excludes removed attachments/groups; historical reports include removed entities.
An empty list is not proof that the requested campaign/group exists.

For creative questions, combine attachment content/role and policy with group and
asset performance. Count unique asset identities separately from attachments.
Reused assets and product partitions overlap: never sum their metrics into campaign
totals. Ad strength/coverage is diagnostic, not causal evidence of sales. Top
combinations have no combination-level spend or ROAS. Signals guide automation;
they do not enforce audience targeting or describe actual delivered audiences.

Use campaign/channel reports for channel spend. Preserve Google's network names,
including unknown future enum values. Placements have impressions only: do not
infer spend or conversions. Conversion-action reports have conversions/value only.
Search terms/categories are privacy-filtered evidence, not a complete search log;
Search keywords and PMax search themes are different. Keep targeted-location
performance separate from the existing country presence/interest breakdown.
Images/YouTube URLs are provider metadata; use authorized asset retrieval for media
and never assume a URL has already been rendered or grants arbitrary fetch access.

### Choose a reporting profile

Use `metric_set=all_conversions` for all conversions/value, `conversion_detail`
for compatible view-through/cross-device totals, `conversion_date` for conversion
occurrence dates, `engagement` for interactions and `video` for video views and
quartiles. Campaign totals also expose watch time; network video rows omit watch
time. These are fixed compatible profiles, not arbitrary field selectors.
Product/video usage reports accept standard metrics only. Detailed search-term
rows accept standard/engagement metrics; use `report=search_term` for compatible
all-conversion totals.

`report=product_attributes` returns categories, product types, custom labels,
country and condition. `shopping_competitive` reports eligible Shopping auction
shares without product segmentation; these are not all-channel PMax shares.
`product_group_brand`, `product_group_category`, `product_group_type`,
`product_group_condition`, `product_group_channel` and
`product_group_custom_attribute` select one partition dimension each. They are
partial views of overlapping partition rows; use `kind=listing_filters` for the
whole configured tree. `sold_product` distinguishes advertised products from
products sold and exposes cart outcomes without invented click/spend values.

`search_term_detail` adds network/device/match-source/targeting-status;
`user_location` describes user geography, distinct from targeted locations.
`expanded_landing_page` describes expanded destinations; the compatible
`landing_page_quality` metric profile returns Google's page diagnostics.
`mobile_platform`, `new_vs_returning`, `conversion_source`, `conversion_lag` and
`click_type` provide campaign breakdowns. Customer status, conversion source and
lag expose conversion outcomes without spend/impressions; mobile platform omits
impressions. These conversion/platform views accept total/daily and
standard/all-conversion metrics only. Unsupported profile combinations fail
with a selection error; do not silently substitute different data or dates.

Conversion-date outcomes and interaction-date spend describe different cohorts.
Do not compute same-cohort ROAS from them without aligning attribution.

### Linked and inherited configuration

Discover `kind=asset_sets`, then pass the selected `asset_set_id` to
`asset_set_assets` or `page_feed_assets`. The set must belong to the selected
campaign; page-feed reads additionally require PAGE_FEED type. Retained removed
links establish historical association, not active usage. These views and account
context reject `asset_group_id`. Feed URLs/labels are configuration inputs, not
served-URL evidence or permission to crawl pages.

Account assets/sets, account recommendations, subscriptions and bid adjustments
are account context. Inspect their explicit campaign, channel and device scopes
before attributing them to the PMax campaign. Simulations are predictions;
experiments are existing metadata. No recommendation is generated/applied and no
experiment or adjustment is created. Filtered experiment/recommendation pages
can be empty while `next_cursor` remains.

Use the existing `list_google_campaign_criteria` for richer campaign exclusions,
`view=customer_negatives` for inherited account exclusions, `view=shared_sets`
for reusable lists (optionally campaign-filtered), and `view=shared_set_criteria`
with `shared_set_id` for members and brand definitions. Keep each collection's
pagination separate and retain provider status/type/unknown values.

Resolve returned location, language or product-category IDs with
`view=reference_definitions`, `reference_type=location`, `language` or
`product_category`, and 1–100 unique numeric-string `reference_ids`. Omit campaign
and shared-list IDs on this view. These are global definitions, not proof of
campaign targeting or eligibility. Product names are localized values in
`data.localizations`; retain language/region rather than inventing one display
name. The lookup does not traverse parent references or other customer accounts.

Use `list_google_conversion_settings` for measurement context: `goal_config`
and `lifecycle_config` require a campaign; `custom_goals`, `lifecycle_goals`,
`customer_types`, `value_rules`, `value_rule_sets`, `tracking`, `upload_client`,
`upload_actions` and `custom_variables` are account context and omit campaign ID.
Cross-account conversion owners remain unresolved resource references; never
switch accounts to follow them. Settings, upload summaries and zero sales do not
prove healthy instrumentation. Audience user-list rules and taxonomy definitions
contain no individual uploaded customer members.

### Product eligibility, audiences and recommendations

Use `list_google_pmax_configuration` with `kind=product_eligibility` for the
selected campaign's current included products, status, prices and issues. These
issues can lag up to 24 hours. This is not historical feed inventory or a complete
Merchant Center audit; a product absent from this campaign may still exist in the
merchant's catalog. Eligibility is campaign-level, without an asset-group filter.

Use `kind=audiences` for definitions referenced by this PMax campaign's audience
signals, optionally within one asset group. This expands inclusion/exclusion
composition plus linked user-list, custom-audience, combined-audience and interest
metadata. It does not retrieve uploaded customer-list members. Custom audience
members are configured keywords, URLs or apps, not individual customers.
Preserve unresolved references as unknown. Combined-audience composition is not
exposed by v25; its name/status metadata may be all that is available. Definitions
remain automation guidance, not proof of observed delivery or audience restrictions.

Use `kind=recommendations` for existing campaign-linked or verified asset-group
recommendations and `kind=budget_recommendations` separately for its budget.
Preserve any multi-campaign association in the returned payload. Shared-budget
recommendations may affect other campaigns; predicted impact is
not observed performance and is not wholly attributable to this PMax campaign.
No recommendation is generated, applied or dismissed. An empty filtered page can
have `next_cursor`; continue it before concluding there are no recommendations.

### Cart and profit reporting

For `list_google_pmax_performance` with `report=campaign`, `product` or `product_group`,
select `metric_set=cart` for primary conversion cart metrics or `cart_all` to
also read the separate all-conversion cart metrics. `standard` remains the default.
The response separates `cart_metrics` and `all_cart_metrics`: never add them
together. Orders and units can be fractional; monetary fields ending `_micros`
are micros, including revenue and gross profit here. Conversion value remains
account currency. Margins and average cart size are non-additive.

Cart sales metrics require conversions with cart data. Profit/COGS metrics also
require product cost-of-goods inputs.
Returned zero does not establish that instrumentation is configured; omitted
fields remain null. Explain missing measurement only when it affects the answer.
Google's attributed product gross profit is not the merchant's net business profit.
Product partition overlap still prevents summing rows into campaign totals.

### Category drilldown and change history

Read `report=search_category` for a campaign's categories and estimated search
volume ranges. Then use `report=search_category_term` with that campaign and one
returned `category_id`, including category zero when returned, for deeper term
insights over at most 31 complete days with total granularity. These insights have
no spend metric. Google privacy and data availability can leave term drilldown
empty while the parent category has metrics. Use `report=search_term` for separate
observed term/spend evidence; do not invent category membership for those rows.
Google retired meaningful search subcategory values in March 2025. v25 still
requires the empty companion field with insight terms; never present it as a
working subcategory hierarchy.

Use `list_google_pmax_changes` for change evidence within explicit account-local
`[start_date,end_date_exclusive)` dates. `view=events` supplies supported old/new
field values within 30-day retention; `view=status` supplies each resource's latest
change within 90 days. The date interface conservatively admits the last 29/89
completed days plus today within those rolling limits. Include today only when
requested and label it incomplete. Neither view is a complete Google UI audit log.

Default `association=campaign` covers directly attributed records. Use
`association=budget` for its verified budget, `asset` with a verified `asset_id`,
or `asset_group` with a verified `asset_group_id`. Shared asset/budget evidence can
involve other campaigns. Asset-group event details are absent from v25; use status.
Each query has Google's 10,000-row cap. If `provider_limit_reached=true`, narrow
dates and read again, including when a filtered final page is empty. Never describe
that bounded result as an unlimited history export. Budget event pages can be
empty with a continuation; keep paging the filtered scan. Change status is not an
ordered log of every edit and has no old/new field values.

Simulated demo brands return explicit PMax unavailability rather than making live
provider requests. Do not imply all Google dashboard insights are available.

## Keyword research

Keyword ideas, historical demand and forecasts are not available through these
tools. Say so plainly, and use the reporting tools above for configured keywords,
observed search terms and campaign spend.

## Create Search ads

Use `check_google_ads_readiness` for account identity, currency and timezone;
this does not prove write access or launch readiness. Use the chosen products
from `list_brand_products` and customer-provided brand facts to draft grounded
Search copy and exact landing-page destinations. Ask only for missing settings:
name, average daily budget, bidding strategy, countries, languages, Search
partners, schedule if wanted, EU political-advertising declaration, keywords and
match types. Ask for countries/languages by name; translate them to codes
internally. The backend resolves Google constants. Targeting supports countries
with presence-based geography, not cities/radii. Do not invent claims, bids,
conversion readiness or a political declaration. Explain that average daily
budget is not a hard daily spending limit. New campaigns include Google Search
and exclude Display. Maximize Conversions requires the customer to understand
and review conversion goals; account read access does not prove measurement works.

Show one compact plan with the selected brand/account, counts, commercial
settings, targeting, keywords, copy and destinations. Say that all new campaigns,
groups and ads start paused and activation needs separate approval. One approval
covers the exact plan; ask again only if material settings change.

1. Call `create_google_campaign` with the account snapshot from readiness and
   approved settings. It creates the budget, campaign and targeting atomically.
2. Read `get_google_campaign` and pass its `write_state` as
   `expected_campaign_state` to `create_google_ad_group`. Manual CPC requires an
   explicit default group CPC in account-currency micros; omit CPC for Maximize
   Clicks or Maximize Conversions. Do not select or switch strategies yourself.
3. Read the group and campaign details. Pass their account and `write_state`
   values to `add_google_keywords` and `create_google_search_ad`. Positive
   keywords use EXACT, PHRASE or BROAD and are enabled only inside the paused
   campaign and paused group; adding them requires both containers paused.
   Responsive Search ads need 3–15 distinct headlines and 2–4 distinct
   descriptions, an HTTPS final URL and optional display paths. Headlines allow
   30 characters, descriptions 90, paths 15; double-width characters count twice.
   No image upload is required. Keep the copy and destination exactly approved.
4. Inspect the created items and report confirmed counts and paused statuses.
   Google review is separate from activation. Do not promise eligibility or
   delivery. If part of the plan failed, report the completed items and stop
   dependent creation rather than claiming the whole plan succeeded.

Keep IDs, codes, fingerprints and account snapshots inside tool calls. The
customer chooses by names or numbered selections. Read changes automatically;
never ask them to supply technical identifiers or to approve readback.

## Change budgets, bids or status

Read details immediately before proposing a change; pass their `write_state`
values and account snapshot. Show exact targets and old → new settings, including
spend/delivery impact, before asking for approval.

- `update_google_campaign` with `change=budget` changes only a dedicated average daily budget;
  shared and total budgets require separate handling in Google Ads.
- `update_google_ad_group_bidding` changes the default CPC only for campaign-level
  Manual CPC without a portfolio strategy. Keyword overrides can take precedence.
  Do not recommend a bid or change the strategy automatically.
- `set_google_status` changes exactly one campaign, group or responsive Search ad.
  Enable/pause is explicit; enabling one level never enables paused items at
  other levels. Enabling a campaign may resume its already-enabled groups/ads.
  Before campaign activation approval, inspect its groups and ads with the existing
  list tools, following pagination. Name groups/statuses, count enabled/paused ads,
  and explain what could resume and what stays paused. If scope is incomplete,
  narrow it before approval; never present a partial inventory as complete.
  Campaign-only approval never enables paused groups or ads. Report paused blockers
  by name, including when the item was already enabled; enabled is not serving.
  For an explicitly approved full setup with a paused campaign, enable selected
  ads → groups → campaign last. Pause a selected campaign first when stopping a
  setup. With an already-enabled campaign, warn that each enable can start spending.
  Refresh detail states between writes. Stop dependent activation on a failed or
  uncertain step and report partial success; never unblock other items implicitly.
  Check configured keywords when diagnosing delivery; paused keywords also block
  matching; use the explicit keyword editing workflow below when a change is approved.

## Add negative keywords

Use `add_google_negative_keywords` with `scope=campaign` to exclude searches across one
Search campaign, or `scope=ad_group` for just one standard
Search ad group. Ask which scope the customer wants when unclear; do not choose
campaign-wide exclusions from an ad-group report automatically. Reuse stable
numbered campaign/group choices. Approval for campaign 2 never includes other
campaigns, shared lists or account-wide exclusions.

Inspect campaign exclusions with `list_google_campaign_criteria`; inspect group
exclusions with `list_google_keywords` and its negative flag. Shared-list tools
provide context but these writes do not edit or attach lists. Read the selected
campaign/group details for the account and current `write_state` values.

Show the exact selected scope, negative text and match types in one compact plan.
Number candidate terms when selection is needed. Confirm only the requested
exclusions; search-term analysis alone is not permission to block searches.
Explain match types briefly when choosing them: exact excludes the matching
query without extra words, phrase excludes the terms together in order with
possible extra words, and broad excludes searches containing all terms in any
order. These rules differ from positive targeting. Do not infer exclusions for
synonyms, singular/plural forms or other close variants. Google accounts for
case and misspellings; do not promise every variation will be blocked.

Send plain text plus an explicit match type, without wrapping brackets/quotes,
in batches of at most 50 per selected target. Enabled and paused campaigns/groups
are supported. Explain that exclusions can affect eligible searches immediately
and may block valuable traffic; do not pause the campaign as a prerequisite or
promise savings. Budgets, bids and statuses remain unchanged.

The tools skip existing same-scope text/match-type exclusions. Report the added
and already-present counts separately; an entirely existing selection needs no
write. A group exclusion and a campaign exclusion have different scope; never
substitute one or treat a shared-list entry as a direct exclusion. A read bound
or changed exclusions means refresh/narrow the scope before another write,
not bypass the check.

For multiple targets, each call is independent. Report completed, already-present
and failed targets separately. Stop on failure or uncertainty and do not expand
scope, remove successful exclusions, or retry automatically. For
`confirmation_pending`, preserve accepted IDs internally and inspect the selected
campaign criteria/group keywords at most twice. For `uncertain`, inspect those
same scoped lists without repeating the write. Explain what remains unconfirmed;
only confirmed exclusions may be reported as saved. Removal requires Google Ads.

## Edit existing Search campaigns and ads

Resolve exact named campaign/group/ad/keyword selections before proposing edits.
Reuse stable numbered choices; “2” selects only that item and does not authorize an edit.
Read settings automatically. Ask only for missing intent or ambiguous scope, not
technical IDs, state values, or permission to perform readback. A request to
inspect or recommend is not permission to edit.

Show the selected target and old → new settings in one compact plan. Name
clears, removals, full-list replacements and possible effects on eligible
traffic. One approval covers that exact plan; ask again only for material changes.
Never change status, pause an active campaign, enable another item or change its
budget as a side effect of an edit. Existing active ads can keep spending while
a selected ad is edited or paused. Google review and enabled status do not prove
serving. Follow the activation workflow separately when activation is requested.

| Customer request                                   | Tool and required read                                                                      |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Change ad copy, URL or display paths               | `update_google_search_ad`; fresh campaign/group/ad details                                  |
| Pause/resume a positive keyword or change its bid  | `change_google_keyword` with `action=update`; `get_google_keyword` and campaign/group details |
| Change keyword text or match type                  | `change_google_keyword` with `action=replace`; the same exact keyword/detail reads          |
| Remove a positive keyword                          | `change_google_keyword` with `action=remove`; the same exact keyword/detail reads           |
| Add country targets/exclusions or remove locations | `update_google_campaign` with `change=targeting`; `get_google_campaign` with `include_edit_context=true` |
| Change weekly serving hours                        | `update_google_campaign` with `change=ad_schedule`; the complete editing context            |
| Change name, Search partners or campaign end date  | `update_google_campaign` with `change=settings`; campaign details                          |
| Change the standard bidding configuration          | `update_google_campaign` with `change=bidding`; campaign details and relevant group/conversion-goal reads |

Keep account, state values and criterion IDs inside tool calls. Editing context
returns campaign and criteria states; keyword details return the keyword state.
Refresh between writes. Stale state or an incomplete context means reread and
reconfirm any changed plan; never bypass the check or guess that an absent item
was removed.

For ad edits, preserve every omitted field. Headline/description arrays replace
the entire list: show the full resulting copy and preserve existing pins unless
unpinning is explicitly approved. Include pin positions from ad details, not just
text. URL-only edits must not resend copy. Describe path/URL clears explicitly.
The tools refuse ads linked outside the selected group. Automatically created
Google assets are separate from the advertiser copy edited here.

For keywords, distinguish pause from removal. Bid edits/clears require standard
Manual CPC; clearing the override restores the group bid. Text/match-type changes
remove/create atomically and do not transfer reporting history. Confirm the
resulting keyword status explicitly; an enabled replacement may affect matching
immediately. The old explicit bid is retained. URL/tracking overrides, labels,
ad parameters or customizer bindings require Google Ads to avoid losing them.
An existing replacement is not permission to remove the original keyword.

Targeting edits change only approved location criteria. Confirm named countries
and exclusions/removals; do not broaden to other campaigns or shared lists.
Removing the final positive location is refused because it could expand reach
worldwide. Language targeting is not an available Search edit.

Weekly schedules are a complete replacement in the account timezone. Explain
that an empty list permits all-week serving, subject to other eligibility rules.
Use 15-minute increments and split overnight intervals across days. Existing
schedule bid adjustments require Google Ads rather than being silently removed.
Clearing a campaign end date can extend serving indefinitely; call that out.

For bidding, show the complete resulting strategy and optional cap/target.
Omitting Maximize Clicks max CPC or Maximize Conversions target CPA removes that
limit/target; never clear one implicitly. Do not choose a strategy, CPA or bid
for the customer. Portfolio/other strategies need Google Ads. A Manual CPC switch
needs confirmed existing group bids; review conversion goals and measurement
before Maximize Conversions. Neither a settings read nor validation proves
measurement health or future performance.

Report `unchanged` separately from saved edits. For multiple targets, calls are
independent: report completed, unchanged, failed and unconfirmed items, and stop
dependent work on failure. Inspect accepted resources with bounded read-only
checks; never repeat removals, replacements or other uncertain writes
automatically. A replacement can be atomic for one keyword while a multi-target
request is only partially complete. Do not claim savings or delivery from a write.

## Recover without duplicate writes

Use returned resource names internally to inspect accepted creations. Never
retry writes automatically: Google does not supply a creation idempotency key
here. `verified` means requested settings were read back; `unchanged` means no
write was needed. For `rejected`, explain that the requested change did not
complete and give a next step. For `confirmation_pending`, Google accepted the
change but the saved settings remain unconfirmed; for `uncertain`, submission
itself is unconfirmed. Check the selected items at most twice with read-only
calls. For an uncertain creation with no resource ID, inspect the relevant
campaign/group/ad/keyword list; matching names alone do not prove identity.
If the result remains unclear, report known completion and ask the user to
check Google Ads or contact support before another write. Never repeat creation
or promise background checking. When settings changed, refresh and reconfirm
rather than replaying the stale plan. Never paste provider errors or credentials.
Use the safe reason and `provider_error_code` to choose the next step, not as
permission to retry. Google gRPC error codes are not HTTP statuses; null
`provider_error_status_code` does not mean the request succeeded. A duplicate-name
error means inspect existing items, not automatically rename and create again.
