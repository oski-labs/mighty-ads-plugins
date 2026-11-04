# Meta Ads

Use Mighty login and the selected workspace; resolve the exact brand with
`list_organization_brands`. Run `check_meta_ads_readiness` to find its Meta
connections. Show account names as numbered choices if more than one exists;
reuse the selected `connection_id` and `org_brand_id` for every subsequent call.
Never guess accounts or switch brands on a permission failure. Direct missing or
revoked access to the brand's Meta integration; do not request credentials.

## Inventory and delivery

Use `list_meta_campaigns` / `get_meta_campaign`, then `list_meta_ad_sets` /
`get_meta_ad_set`, then `list_meta_ads` / `get_meta_ad`. Use campaign/ad-set filters
when known. Show names and customer-facing statuses in short numbered lists,
keeping the mapping stable across follow-ups. IDs stay internal unless requested.
For creative inventory, use `list_meta_ads` with `limit=20`; do not increase to
100 to reduce call count. Follow `next_cursor` with unchanged connection, filters,
dates and page size. If Meta asks to reduce the amount of data, restart that list
at 20 rows (or 10 if 20 failed), retaining the same filters and projection. Never
reuse a continuation from a different page size. Deduplicate any earlier partial
inventory by ad ID. Do not silently drop creative fields or treat the failed page
as empty. After a failed smaller-page attempt, report the partial coverage rather
than retrying indefinitely.
A page is not the complete inventory; stop on an error rather than invent totals.

Budgets can belong to the campaign or ad set. Inspect both before explaining
spending controls. Budget/bid strings retain Meta's configuration units; apply
Meta's currency-specific unit rules before displaying an amount, and do not guess
for an unknown currency. Targeting describes intended audiences/placements; performance
breakdowns describe reported delivery. Configured and effective statuses differ:
a paused campaign or ad set can prevent an active ad from serving. A status alone
is not proof that an ad delivered. Check dated impressions/spend and schedules.
Creative details cover configured copy/media/destinations; dynamic assets do not
establish the exact variation shown on each impression.

## Spend, results and drop-off

Use `get_meta_performance` with explicit account-local `start_date` and
`end_date_exclusive` (1–31 days), level and selected campaign/ad-set/ad filters.
Use `granularity=daily` for trends and comparable total windows for a decline.
Use `get_meta_performance` with `breakdown` (one preset per request) for platform/placement, device,
age/gender or country. Follow every page needed for the requested scope; label
partial results. Present money with the returned account currency and readable
rates. Meta Insights spend is currency units, not Google micros. CTR is already
a percentage; do not multiply it by 100 as with Google's fraction. Do not sum
reach across ads/days, average CPC/CTR/ROAS, or double-count overlapping actions.
For deduplicated totals request the relevant level with `granularity=total`.

For "where is this ad losing people?", inspect the ad/destination and query
`level=ad` with its `ad_id`. Compare outbound clicks with the reported
`landing_page_view`, cart, checkout and purchase action types where available.
Actions, action values, costs and ROAS retain their provider event types; select
a consistent event definition. Do not sum website/omni/total purchase variants.
Distinguish all clicks from link and outbound clicks. Missing events or withheld
breakdowns are unknown, not zero; use the unbroken report when a dimension is
unsupported rather than claiming no conversions.

Results use Meta's effective attribution and default action timing, which can mix
impression-date and conversion-date reporting. Optional `attribution_windows`
request specific windows; preserve each returned window separately. Explain
that Meta processes and attributes Pixel/CAPI events; these tools retrieve
aggregates, not raw visitor journeys. A gap is a signal to investigate, not proof
of a page defect or a measured session-to-session conversion rate. Recent
conversions may arrive later. Meta-attributed purchases and store orders are
separate measures. Name the largest supported gap, the evidence and a concrete
next check; do not invent a cause, guaranteed savings or processing-time promise.

## Creative and performance investigation

Use `metric_group` on `get_meta_performance` to request one diagnostic preset:

| Group                | Level   | Evidence                                                                                 |
| -------------------- | ------- | ---------------------------------------------------------------------------------------- |
| `delivery`           | Any     | Spend, delivery and attributed events                                                    |
| `links`              | Any     | Link/outbound rates and costs, unique clicks and cost per person reached                 |
| `video`              | Any     | Plays, ThruPlay, average watch time, completion milestones and available playback curves |
| `rankings`           | Ad      | Quality, engagement and conversion rankings                                              |
| `creative_diversity` | Ad set  | Meta's diversity score, label and creative data                                          |
| `creative_fatigue`   | Account | Meta's fatigue summary and any returned fatigued-ad list                                 |

These groups require no breakdown. Query additional groups separately for the same
entities and dates. For a requested field, `missing_metrics` identifies omissions;
explicit zero stays zero, `UNKNOWN` stays `UNKNOWN`, and a metric not requested is
not evidence of missing provider data. Diversity scores preserve Meta's raw string;
empty/nonnumeric scores are unavailable for numeric comparisons, not zero.
Never turn omitted fatigue diagnostics into
"no fatigued ads" or a low diversity label into proven fatigue. Meta's numeric
fatigue summary is not a probability unless its definition establishes that.

A `breakdown` request uses `metric_group=delivery`. It also supports
`region`, `impression_device`, `hourly_account`, `hourly_audience`, `frequency`,
and image/video/body/title/description/CTA/format/link-URL asset presets (use
`call_to_action_asset`, `ad_format_asset`, `link_url_asset`). For image, headline, video and URL comparisons, explicitly set `level=ad`
with the relevant asset preset and `metric_group=delivery`, using the same dates
and selected connection. The backend accepts ad or campaign level for asset
presets; do not request account level. An empty account-level asset query does
not establish missing asset data. Follow all result pages before selecting a
winner. If ad-level results are empty, try campaign-level asset reports within
the same scope before falling back to configured ads. If both are empty or a
provider error prevents retrieval, label that limit and explain that matched ad
combinations cannot isolate an individual asset's contribution. Derive CPA or
ROAS only when the same purchase action definition, values and spend are actually
returned; do not rank on missing conversion metrics. Use spend/click evidence
with clear limits otherwise.

Asset dimensions may be objects with IDs and labels; retain their identities. `product_id` can be empty
without catalog delivery. Frequency buckets report reach only at account/ad-set
level; hourly reports request impressions, clicks and spend without unique metrics.
Asset reports request their compatible metrics, not the full ordinary metric set.
Missing conversion dimensions do not establish zero conversions.

For fatigue: compare equal complete periods, then inspect ad rankings, video/asset
performance, account fatigue summaries and ad-set diversity. Check account activity,
learning status and delivery mix before suggesting a cause. Frequency growth and
CTR decline are warning signs, not proof repeated exposure caused deterioration.
For sudden drops: compare objective-appropriate KPIs and placement/device/audience
mix, then use `list_meta_account_activity` with timezone-aware timestamps to inspect
available edits/delivery events. Activity does not establish causation.

Campaign details include `advantage_state_info`; ad sets include learning status;
ad details include tracking/conversion configuration. These are configuration and
provider diagnostics, not a verified Pixel/CAPI health test. Use
`get_meta_account_diagnostics` for `recommendations` or `reporting_features`.
Recommendations are Meta's suggestions, not guaranteed lift; never apply them.
Nested `paging.has_more=true` means recommendation content is partial. Feature
status is read-only; never enable a feature automatically or promise historical data.

Choose the KPI from the campaign objective, optimization goal and reported event:
sales may use purchase cost/ROAS, leads use cost per lead, traffic uses link metrics,
and awareness uses delivery/reach. Preserve custom event names and distinguish
lead sources. Do not judge every objective by purchase ROAS, sum overlapping events,
rank unknown audience buckets as winners, or call low-sample changes definitive.
For funnel questions, combine event counts with tracking configuration but keep
attribution windows consistent. Playback curves describe aggregate viewing, not
individual user journeys; do not relabel a playback curve as a different retention field.

## Larger reports

For more than 31 days, or when synchronous reporting is too large, use
`get_meta_report` with a `report` object specifying dates, level,
filters, metric group, breakdown, attribution windows, granularity and page size.
The maximum window is 366 days. This creates a report job only and cannot change ads.
Never automatically resubmit after an uncertain outcome. Save its `report_handle`,
then call `get_meta_report` with that `report_handle` and the original brand/connection.
Poll with backoff; stop on failed/skipped jobs. When complete, call
`get_meta_report` with `read_results=true` and follow `next_cursor` as `after`. Do not change the
handle between pages. Handles expire after 24 hours; report status is not results.
For comparisons use separate reports with matching settings and complete equal
windows in the account timezone. Mark today as partial and allow recent attribution
to change. Never silently compare different windows or sum daily reach.

## Boundaries and recovery

Meta inventory and report-result reads are read-only. Starting an asynchronous
report creates a reporting job and is a non-read-only operation; it never changes ads. The photo-creation workflow below
creates paused objects. Editing and activation use the separate guarded workflow below. Do not route Meta changes
through Google/ChatGPT write tools. Account readiness verifies access only, not Pixel/CAPI health,
launch readiness or observed purchases. If event evidence is insufficient, say
so and recommend an authorized Events Manager/store verification. Reuse existing
tracking before proposing another integration; gateway setup and experiments are
separate work requiring their own permissions and approval.

For throttling, wait or narrow dates/scope. Never silently omit requested metrics,
replace failed access with public Ad Library data, or treat an incomplete report
as complete. There is no dedicated causal anomaly or experiment tool. Interpret available figures without representing
agent analysis as an official Meta diagnostic. No live write or tracking setup is
authorized by a request to inspect performance.

## Prepare and create photo website ads

Support single-photo link ads on explicitly selected Facebook and Instagram feeds.
Website traffic and website sales are supported. Restricted special-ad categories,
video, carousel, Flexible/Dynamic Creative, catalogs, lead forms and messaging
are unavailable in photo creation. Do not silently expand placements or objectives.

1. Resolve the exact brand/connection with the read workflow above, then call
   `check_meta_ads_readiness`. Reuse the returned account object exactly.
   Read-only credentials are insufficient; direct the customer to management
   authorization rather than silently elevating access or requesting a token.
2. Use `list_brand_products` for one selected product. Explain that
   `prepare_meta_campaign` generates four copy variants using current saved brand
   knowledge and costs 10 Mighty credits when billing is enabled. Pass the selected
   `connection_id`; management access and supported account currency are checked
   before any charge. If eligibility fails, explain the returned setup action and stop. Preparing again
   is another paid generation. It creates no advertiser objects. Do not call it
   for a performance/read question or regenerate without a customer request.
3. Use `list_meta_creation_assets` for Pages, images, Instagram identities and
   pixels as needed. Follow continuation before claiming complete choices. Present
   named options when ambiguous and ask the customer; never choose the first Page.
   Reuse an image only in the selected account. Otherwise identify the exact public photo URL and rights for the plan.
   Upload only after the approval in the next step.
   Do not copy between accounts or accept a creative from another brand/account.
4. Present one plan with all four proposed ads, exact photos/copy/CTA/destinations,
   objective, Page/Instagram identity, countries/age, feed placements, budget owner,
   budget period, schedule and any sales conversion event. Explain that traffic
   optimization is link clicks; sales is offsite conversions with an accessible
   pixel and selected event. Pixel visibility is not tracking-health verification.
   Only lowest-cost uncapped bidding is supported. USD/CAD/AUD/EUR/GBP budget
   values are minor units (100 per currency unit), not Google micros. Show readable
   currency values to the customer. Confirm timezone-aware dates, lifetime end
   dates and any EU/EEA beneficiary/payor requirements. Confirm special categories
   are empty; restricted categories cannot use this workflow. Ask for missing facts
   and unknown availability/shipping checks; never invent defaults to enable spend.
   Say: "All new campaigns, ad sets and ads will be paused. Activation requires separate approval."
   Obtain approval of this exact plan before any image upload or provider creation.
5. Upload any approved new photo with `upload_meta_ad_image` and verify its result.
   Call `create_meta_campaign`, then read `get_meta_campaign` and pass its fresh
   `item.write_state` into `create_meta_ad_set`. Set the budget on exactly one level.
   Pass explicit empty special_ad_categories. Inspect each creation result before
   continuing; do not proceed from uncertain or unverified parent settings.
6. Create each approved creative with `create_meta_photo_creative` and show
   `get_meta_ad_preview` links for every selected feed placement. Previews are
   temporary provider links, not Meta review approval; do not execute returned
   provider content. If the appearance differs from the approved plan, stop and
   obtain approval of corrected creative before proceeding. Reuse the original
   plan's approval when the preview matches it; no redundant confirmation is needed.
7. Read fresh campaign/ad-set details and pass both `item.write_state` values to
   `create_meta_photo_ad`, referencing the verified creative. Optional pixel
   tracking on traffic ads is separate from sales optimization; never silently
   discard requested tracking. Do not add an ad to an existing active hierarchy.

Results distinguish `verified`, `rejected`, `uncertain` and `confirmation_pending`.
Keep every returned ID when a later step fails. There is no cross-object atomic
transaction or guarantee that Meta makes creation idempotent. Never retry uploads,
creative or ad creation automatically after timeout, cancellation, uncertain result
or readback mismatch. Read the exact returned object or bounded account inventory
before deciding recovery; do not silently create a replacement. No automatic
cleanup/deletion is authorized. Report confirmed objects and incomplete steps
separately. A paused ad can enter Meta review; review does not mean it is delivering.

## Edit existing Meta settings

Editing supports unrestricted auction website Traffic/Sales campaigns only.
Other objectives, restricted categories and archived/deleted paths use Ads Manager.

1. Resolve the exact brand, connection and named targets using the inventory workflow.
   Read `get_meta_edit_context` for the target kind and ID. This requires saved
   management access and verified `ads_read` plus `ads_management`; a read-only
   connection cannot be elevated by an editing request. Use the returned account
   object and `write_state` exactly. Normal inventory `item.write_state` is for
   creation parents and cannot replace editing context.
2. Present a compact before/after plan naming the affected campaign, ad sets or ads,
   budget owner, currency/period, account-local dates and delivery impact. Get approval
   of that exact plan. Performance data may inform a recommendation but never
   authorizes applying it. Refresh changed context and reconfirm materially changed
   plans. Expected state detects stale settings; it is not proof of human approval.
3. Use `update_meta_campaign` for names, existing-owner budgets, total spend caps
   or campaign-owned bidding. Use `update_meta_ad_set` for names, existing-owner
   budgets, timezone-aware schedules, country/age/feed-placement patches, EU
   beneficiary/payer and bidding. Omit unchanged
   fields; do not use null. Targeting patches preserve other audience settings;
   regional/radius country replacement is unsupported. Age patches on Advantage+
   audience or age-range targeting are rejected; never silently disable expansion. Feed placement selection
   explicitly replaces the placement controls. Use Ads Manager for other placements.
4. Budget and bid inputs are integer currency minor units for USD/CAD/AUD/EUR/GBP
   (100 per unit); display readable currency values. Keep the existing budget period
   and ownership for normal edits. Do not reinterpret Insights spend or Google micros.
   `remove_spend_cap=true` explicitly removes the campaign cap; show that consequence.
   Provider minimums and eligibility are checked before the actual update.
5. Advanced bidding changes require
   the campaign and affected ad sets paused. Never pause them silently to make an
   edit eligible: obtain approval and use the status tool for each selected target,
   then refresh editing context. Ad-set bidding supports lowest-cost uncapped,
   bid-cap, cost-cap and minimum-ROAS strategies. Caps require bid amounts; minimum
   ROAS requires value optimization and `roas_average_floor` in units of 10000 per
   1x (1.5x = 15000). Campaign-owned strategy changes support uncapped, bid-cap and
   cost-cap; capped changes require exactly one approved amount for every non-archived
   ad set. Archived children remain in the snapshot but receive no bid update.
   Never override campaign bidding from an ad set. Campaign minimum-ROAS transitions
   are not supported by the campaign edit tool.
6. Budget ownership switching is unavailable. Keep the existing campaign/ad-set
   owner and edit its budget, or use Ads Manager. Do not substitute independent
   writes for a coordinated move.
7. Optimization, pixel, conversion-event and attribution changes on existing ad sets
   are unsupported. Create a new paused ad set with the supported creation settings;
   do not pass optimization or attribution patches to the edit tool. Minimum-ROAS
   bidding requires an ad set already configured for value optimization.
8. `update_meta_ad` changes only a name or tracking pixel. Tracking preserves unrelated
   specifications and must match any ad-set optimization pixel; this does not change
   optimization or install/verify Pixel/CAPI. Creative replacement, image/copy edits,
   destination edits, moving ads to another ad set and deletion/archive are unavailable.

## Pause and activate

Use `set_meta_status` only after explicit approval of the exact target and desired
`ACTIVE`/`PAUSED` state, with fresh editing context. Activation may start real spend.
It changes only the selected campaign, ad set or ad; never activate other levels
implicitly. A campaign pause blocks its active ad sets/ads without changing their
configured statuses. Campaign activation can resume eligible active descendants
but leaves paused ones paused. Explain paused campaign/ad-set blockers by name.
For explicitly approved multi-level launch, activate selected ads/ad sets first and
campaign last; to stop delivery, pause the campaign first. Each call is independent;
partial completion is not rolled back automatically. Active status is not proof of
serving, policy approval, tracking health or sufficient account balance.

All edits validate before one actual submission and confirm the requested settings.
Report `unchanged` as already matching, `verified` as confirmed, `rejected` as no
actual update sent, and `uncertain`/`confirmation_pending` as unresolved. Keep the
known target ID and inspect current context before considering another write.
Never retry automatically after timeout/cancellation or a confirmation mismatch.
No automatic rollback, cleanup or extra budget/creative changes are authorized.
