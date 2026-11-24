# Microsoft Advertising

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_microsoft_ads_readiness` to find its
Microsoft Advertising connections. Each connection is one advertiser account.
Show account names and numbers as numbered choices if more than one exists;
reuse the selected `connection_id` and `org_brand_id` for every subsequent
call. Never guess accounts or switch brands on a permission failure. Direct
missing or revoked access to the brand's Microsoft Advertising integration; do
not request credentials.

Readiness reads the account live, re-checks the connecting Microsoft user's
role and runs one campaign read. If the role was removed, the user is now a
Viewer, Microsoft refused the account, or the account is Draft, Inactive,
Suspended or paused by the advertiser, readiness says so in `next_step` instead
of failing: relay it and point the customer to the account's Super Admin or to
Reconnect. A read-only connection cannot be elevated by asking; reconnecting
with management access is a Console step. `write_access_checked` is always
false: readiness does not test changes. When `environment` is `sandbox`, say
that sandbox ads never serve and spend nothing.

Reads change nothing. Microsoft Advertising serves Bing, Microsoft Start, Edge
and partner search; Microsoft's own Copilot has no advertising API, so never
promise Copilot placement or a Copilot setting. Never route Microsoft requests
through Google, Meta or other channels' tools, even though the account mirrors
Google Ads. Changes use the separate workflows below, only on a manage
connection with `management_permission_granted=true` and only after the
customer approves the exact plan. Search campaigns only: Shopping, Audience,
Performance Max and other types, shared budgets and lists, audiences and
deletion are not available here.

## Inventory

Microsoft lists by parent: `list_microsoft_campaigns` / `get_microsoft_campaign`
for the account, `list_microsoft_ad_groups` / `get_microsoft_ad_group` for one
`campaign_id`, and `list_microsoft_ads` / `get_microsoft_ad` and
`list_microsoft_keywords` / `get_microsoft_keyword` for one `ad_group_id` (pass
`campaign_id` too when you have it). To find an ad group across the account,
list campaigns first and then their ad groups. Show names and statuses in short
numbered lists, keeping the mapping stable across follow-ups. IDs stay internal
unless requested. Follow `next_cursor` with unchanged connection, filters and
page size; a page is not the complete inventory. A positive `skipped_items`
means Microsoft returned rows that could not be read: say the list is
incomplete.

Budgets and bids are decimal amounts in the account currency: `daily_budget`
25.0 USD is $25.00 per day, and a `budget_type` of `LifetimeBudgetStandard`
makes that amount a lifetime budget. `shared_budget_id` means the campaign
spends from a shared budget instead. `campaign_type` tells Search from
Shopping, Audience (Microsoft Audience Network), Hotel, Performance Max, App
and ObjectiveBased campaigns; `bidding_scheme` is Microsoft's strategy name,
for example `EnhancedCpcBiddingScheme` or `MaxClicksBiddingScheme` with an
optional `max_cpc` cap. `status` is what the account set (Active or Paused);
`BudgetPaused`, `BudgetAndManualPaused`, `Suspended`, `Expired` and `Inactive`
are set by Microsoft, so explain them as Microsoft's reason. Ads and keywords
carry `editorial_status`: `Disapproved` means Microsoft rejected it, `Inactive`
means review is pending or failed, and `ActiveLimited` means it serves in some
markets only. Responsive search ads carry their headlines and descriptions with
pins; other ad types carry their type and status only. Keywords show text,
match type (Exact, Phrase or Broad) and a bid that, when empty, means the ad
group's `cpc_bid` applies.

`list_microsoft_negative_keywords` lists the negatives assigned directly to one
campaign, or to one of its ad groups with `ad_group_id`. Negatives are Exact or
Phrase only. For a campaign, `shared_lists` names the shared negative keyword
lists that also block traffic; their items are managed in Microsoft
Advertising's shared library and are not listed here, so say so when asked
whether a term is excluded.

## Spend and results

Microsoft only reports performance through report jobs, so each read may take a
moment:

1. Call `list_microsoft_performance` with account-local `start_date` and
   `end_date_exclusive` (1–366 days), `level` and `granularity` total or daily.
   `account` gives totals; `campaign` lists every campaign or up to 20
   `entity_ids`; `ad_group` needs one `campaign_id` (or `entity_ids` with their
   `campaign_id`); `ad` and `keyword` need one `campaign_id` or one
   `ad_group_id` with its `campaign_id`.
2. The call waits up to about 40 seconds. If `status` is `pending`, keep the
   returned `report_handle`, tell the customer the report is still running,
   and call the tool again with the same arguments plus `report_handle` about a
   minute later; never resubmit without the handle, and never loop more than a
   few times in one turn. Handles expire after 24 hours.
3. When `status` is `complete`, follow `next_cursor` as `after` with the same
   `report_handle`, connection, arguments and page size before quoting totals.

Metrics are impressions, clicks, spend, average CPC, CTR, conversions, all
conversions, conversion rate, cost per conversion, revenue and return on ad
spend. `spend` and `revenue` are in `currency_code`. `conversions` are
Microsoft's qualified conversions from Universal Event Tracking (UET) goals that
count toward bidding, `all_conversions` every goal; they are not store orders,
and revenue is advertiser-reported, not store revenue. `ctr` and
`conversion_rate` are percentages as Microsoft reports them. `missing_metrics`
lists metrics Microsoft did not return; they are unknown, not zero. Dates are
days in `report_time_zone`, the account's time zone. Microsoft makes clicks
available within about two hours and conversions within three and can adjust
for invalid traffic later: label the latest day as provisional, call it partial
when `includes_today` is true, and say so when `potential_incomplete_data` is
true.

`list_microsoft_search_terms` reads the search terms that triggered ads in one
`campaign_id`, or one of its ad groups with `ad_group_id`, with the matched
keyword, `match_type` (the bid) and `delivered_match_type` (how the query
matched, including close variants). It uses the same handle and paging flow.
Microsoft includes only terms with a significant number of clicks in the last
30 days, so present it as a sample for negative-keyword candidates, not every
query.

## Boundaries and recovery

Readiness verifies account access, the role and one campaign read only, not
UET conversion tracking, launch readiness or observed purchases. If event
evidence is insufficient, say so and recommend UET setup in Microsoft
Advertising.

If a report fails, Microsoft could not build it: narrow the dates or scope and
run a smaller one rather than retrying the same request. On a rate-limit error,
wait a minute before retrying or narrow the request; never retry in a loop. If
Microsoft refuses Mighty's developer token, that is a Mighty configuration
problem: report it rather than asking the customer to reconnect. If a read fails
after account access changed, direct the customer to Reconnect on the Microsoft
Advertising integration card. Never present a partial page as the whole
account, invent totals, or quote raw provider codes.

## Create paused Search campaigns, ad groups, keywords and ads

Microsoft creation uses the manually planned workflow below. Paid,
product-grounded Quick Campaign proposal preparation is deferred to a separate
PR; no Microsoft proposal-preparation tool is available. Explain this boundary
when a customer requests Quick Campaign, then offer the manual planning flow.

1. Resolve the brand and connection with `check_microsoft_ads_readiness`; it
   must show a manage connection with `management_permission_granted`.
   Read-only connections cannot be elevated by asking; reconnecting with
   management access happens in Console.
2. Collect the campaign name, a daily budget in the account currency (at least
   0.05 for most currencies), the bidding strategy (Enhanced CPC, Maximize
   Clicks or Maximize Conversions; Manual CPC and Target CPA/ROAS do not exist
   on Microsoft Search), ad languages by name and the countries to target. Ask
   for countries and languages by name and translate them internally. Then
   for each ad group collect the name, the default bid (Enhanced CPC only),
   the network (the whole Microsoft network or Microsoft sites only) and
   optional dates in the campaign's time zone, the keywords with match types,
   and the responsive search ad copy: 3–15 distinct headlines of up to 30
   characters, 2–4 descriptions of up to 90, optional pins and display paths,
   and one HTTPS landing page.
3. Present one compact plan with those settings and say: "All new items will
   be paused. Activation requires separate approval." Political ads are
   refused by Microsoft; say so instead of trying. Obtain approval of that
   exact plan before any creation.
4. Call `create_microsoft_campaign`; countries are applied as location targets
   in a second call, and a `confirmation_pending` result with a campaign ID
   means the campaign exists paused but untargeted, so do not create it again.
   Pass the returned `item` (or a fresh `get_microsoft_edit_context` campaign)
   unchanged to `create_microsoft_ad_group`, then that result's `item` with the
   campaign to `add_microsoft_keywords` and `create_microsoft_search_ad`.
   Keyword batches report each keyword in `items` with Microsoft's reason when
   refused; relay partial results honestly. New ad groups cannot serve until
   they have keywords and an approved ad.

## Change settings and status

1. Read `get_microsoft_edit_context` for the target (campaign; ad group with
   its `campaign_id`; keyword or ad with `campaign_id` and `ad_group_id`) and
   pass its `account`, `campaign`, `ad_group` and `item` unchanged; do not
   edit or rebuild them. Each change re-reads the settings it depends on and
   sends nothing if they changed since the read, so an unrelated edit does not
   block a pause.
2. Present a before/after plan naming the affected item, readable amounts in
   the account currency and the delivery impact, and get approval of that
   exact plan.
3. Use `update_microsoft_campaign` with `change` budget (daily budget;
   campaigns on a shared budget are changed in Microsoft Advertising),
   settings (name, languages, which replace the list) or bidding.
   `update_microsoft_ad_group` changes the name, default bid, network or
   dates, or clears the end date; a start date that has arrived cannot change.
   `change_microsoft_keyword` pauses, activates, re-bids or clears the bid of
   one keyword; text and match type cannot change, so add a new keyword and
   pause the old one. `update_microsoft_search_ad` edits copy, paths and the
   final URL; supplied headline or description lists replace the whole list.
   `add_microsoft_negative_keywords` adds Exact or Phrase negatives to a
   campaign or one ad group, skipping ones already present.
4. Use `set_microsoft_status` only after explicit approval of the exact target
   and the desired Active or Paused state. Activation may start real spend and
   changes only the selected item: activating a campaign does not activate its
   ad groups, keywords or ads, and the result names what still blocks serving.
   `BudgetPaused`, `Suspended`, `Expired` and `Inactive` are set by Microsoft
   and cannot be set here. To stop delivery, pause the campaign first.

Results report `verified`, `unchanged`, `rejected` (Microsoft refused, so
nothing was applied), `confirmation_pending` (accepted but not yet confirmed)
or `uncertain` (the submission may or may not have applied). Microsoft has no
validate-only mode and no idempotency guarantee, and it refuses duplicate
campaign and ad group names: never retry creation or changes automatically.
After an uncertain creation, list the account's campaigns, the campaign's ad
groups or the ad group's keywords and ads and look for the name before
anything else. When Microsoft refused because the settings changed first
(error 4149 or a changed-since-read message), read the editing context again
and confirm the new plan.
