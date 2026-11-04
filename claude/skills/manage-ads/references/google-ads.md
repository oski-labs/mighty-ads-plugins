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
