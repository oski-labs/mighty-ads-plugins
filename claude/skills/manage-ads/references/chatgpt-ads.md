# ChatGPT Ads

## Live reads

| Need                    | Tools                                                      |
| ----------------------- | ---------------------------------------------------------- |
| Campaigns and settings  | `list_chatgpt_campaigns`, `get_chatgpt_campaign`           |
| Ad groups and bidding   | `list_chatgpt_ad_groups`, `get_chatgpt_ad_group`           |
| Ads and creative        | `list_chatgpt_ads`, `get_chatgpt_ad`                       |
| Actual spend            | `list_chatgpt_performance`                                 |
| Provider conversions    | `list_chatgpt_performance` with `include_conversions=true` |
| After-ad-click activity | `get_chatgpt_post_click_outcomes`                          |
| Campaign or account spend review | `get_chatgpt_spend_opportunities`                   |
| Mighty workspace links  | `list_chatgpt_campaigns` (`linked_to_mighty` on each campaign) |

Resolve names within the selected brand's live campaign list, then within that
campaign's ad groups. Ask when names are ambiguous. Paginate with `next_cursor`
as `after` until `has_more` is false. Stop on missing/repeated cursors or failed
pages and label the inventory incomplete; account-wide `all` requires complete inventory.
For an ordinary campaign overview, after all pages have been read, show newly
created campaigns first using provider `created_at` (fall back to `updated_at`
only when creation time is unavailable). Never sort just the first provider
page and call it the account's latest campaigns. Show a short numbered first set and
continue from the complete sorted set when the user asks to see more.
Keep selection numbers stable within that list; label a new list before renumbering.
“All” can select all displayed choices; an account-wide “all” requires complete
inventory. Ask if the intended list or scope is ambiguous. Missing performance
or a failed read is unavailable, not zero activity.

Report account, currency, relevant status and when settings were checked in
readable language, not raw timestamps. Convert
micros to account-currency amounts by dividing by 1,000,000. Active status does
not prove delivery; budgets are limits, not spend. Published provider settings
are authoritative. Missing targeting/event availability flags or a null campaign
mode mean unavailable, not empty. Workspace links do not prove creation origin.

Performance uses completed account-local days and an exclusive end date. On
continuation, keep the first page's returned dates unchanged. Only total complete,
numeric rows at one aggregation level; do not mix campaign/group/ad sums or hide
provider rounding differences. Delivery rows do not provide revenue or conversion
counts. Do not calculate ROAS or recommend bidding based on invented performance.

For “were there conversions?” or conversion changes, call
`list_chatgpt_performance` with `include_conversions=true` and explicit dates.
Use `conversion_summary` as the authoritative provider-reported campaign goal
counts. `conversions` includes click-through and view-through counts; report the
returned split without adding those counts to the total again. The summary
covers the whole campaign and reporting interval, even with ad-group/ad rows or
pagination; never sum it across pages or present it as a per-ad breakdown.
Its attribution basis is ad interaction date, with a 30-day click window and
one-day view window. State the period and keep comparable windows for declines.
Answer the count first, then describe Mighty-attributed Shopify orders separately
if requested or needed to explain a discrepancy. Provider goal conversions are
not necessarily purchases. Do not replace provider totals with Shopify orders,
add the two sources, or infer a tracking cause from their difference. If the
summary is absent, the tool lacks this option, or reporting fails, say provider
conversions are unavailable; never substitute zero or reuse an earlier count.
`get_chatgpt_campaign_status` and `get_chatgpt_campaign_delivery` read Mighty workspace
evidence and accept authorized OAuth or agent-run callers. They do not replace
the live reporting tools above. If a required tool is unavailable or authorization
fails, explain what is unavailable and stop; stored Mighty campaigns do not replace
live reads.

For a campaign spend-review question, call `get_chatgpt_spend_opportunities`
with its campaign ID. For an account-wide question, call
`get_chatgpt_spend_opportunities` without a campaign ID. It compares
the complete connected inventory up to 20 campaigns and fails clearly above
that bound; then ask the user to choose a campaign for a focused review. The
default covers the last 14 completed advertiser-local days; an explicit
interval must stay within 31 days. Do not call a partial sample a complete
account review. Report the period, currency, evidence basis, and only returned
promising/review findings at the campaign, ad-group and ad levels. An
`insufficient_data` status means no ranking is supported at that level; a
campaign may still show historical facts. Paused or ended campaigns can have historical
findings; these are not live pause recommendations. If the basis is
`engagement_only`, describe CTR as engagement, not sales or profit. Attributed
orders are observed click-linked orders, not all purchases.

Keep historical findings separate from `pause_recommendations`. Show a pause
candidate only when returned by that field. Its seven-day estimate means the
recent seven-day ad spend might be avoided if the same pace continued; it is
not a guaranteed saving, and the campaign budget may reallocate. Do not sum
candidate estimates into a guaranteed account saving or invent an estimate
when the tool returns none. A recommendation is read-only. If the user wants to
proceed, show the exact ad and effect, reread the live campaign/ad group/ad
settings, and obtain explicit confirmation before calling `set_chatgpt_status`
once per selected target. Multiple status calls are not an atomic one-click
batch; report partial outcomes honestly.

For “what happened after clicks,” use `get_chatgpt_post_click_outcomes` for the
selected campaign. It reports exact campaign-linked Shopify page and product views,
add-to-cart events, checkout starts, and paid orders for completed
advertiser-local days. State the period and latest measurement time. These are
event counts, not unique shoppers or a cohort funnel; page views are not proven
landing-page arrivals. If status is `unattributed` or `unavailable`, explain
the measurement gap rather than reporting zero conversions. Do not combine
unlinked store activity with campaign-attributed stages or infer that every
provider click produced a site event.

## User-requested bidding changes

Read the selected campaign and ad groups before confirmation. Bids belong to
ad groups, not campaigns. Use `update_chatgpt_ad_group_bidding` once per selected
group, with the same connection and `org_brand_id`:

- `account_id`: from live reads.
- `campaign_id`, `ad_group_id`: the confirmed targets.
- `expected_campaign_updated_at`: the campaign's returned `updated_at`.
- `expected_ad_group_updated_at`: the ad group's returned `updated_at`.
- `expected_bidding_config`: the group's returned `bidding_config`, unchanged.
- `request.bidding_config`: the user's desired configuration.

For `fixed_bid`, supply `billing_event_type` (`click` or `impression`) and a
positive integer `max_bid_micros`. Clarify CPC versus CPM if ambiguous; do not
silently change billing type. Preserve existing audience multipliers by omitting
that field unless the user explicitly requests a change. For `maximize_clicks`
or `maximize_conversions`, use click billing, omit the bid amount and clear
`custom_audience_bid_multipliers` to `[]`; disclose that clearing when relevant.
For a bid-only change, retain the current strategy; automatic strategies have
no fixed bid amount. Provider objective/budget compatibility may reject a change;
never change campaign settings to work around rejection.

Translate result codes into customer language:

- `verified`: “I checked—[name] now has [requested setting].”
- `unchanged`: “It was already set that way; no change was needed.”
- `rejected`: “OpenAI couldn't apply the change.” Explain only a known reason.
- `uncertain`: “I couldn't confirm whether the change went through.” Check current
  settings without making another change, explain what is known and stop.

If settings changed since confirmation, show them and ask again. Do not repeat
technical errors, claim success without confirmation or invent rejection reasons.
Campaign budget, objective and status are not edited by the bidding tool.

## Status changes

Use `set_chatgpt_status` for one campaign, ad group or ad: pause, deactivate,
disable or turn off → `paused`; activate, resume, reactivate, enable or turn on
→ `active`. Clarify ambiguous “stop/delete/remove”; never interpret these as
permission to archive. “Group” means ad group within the selected campaign.
Read the full campaign → group → ad path as applicable. Send
`account_id`, `entity_type`, `campaign_id`, the applicable `ad_group_id`/`ad_id`,
and ordered `expected_hierarchy` snapshots containing each live resource's
`entity_type`, `id`, `name`, `status`, `updated_at`. Preserve the selected brand.
Membership must be verified; a missing parent ID is not proof of ownership.

Before campaign activation, show each group's name/status and live ad counts
by status (active/paused; archived separately), not every ad's copy. Identify
which active groups could serve eligible active ads. Explain that activation does not
activate paused groups or ads; include ad groups/ads beneath the campaign only
if explicitly requested, then list and confirm those exact targets. Paused
groups/ads stay paused. Pausing a campaign blocks its groups and ads from serving;
pausing an ad group blocks its ads. Their individual statuses do not change.
Activating an ad group or ad under a paused campaign/ad group does not unblock
delivery: name the blocking campaign/ad group and ask whether to activate it,
never do so implicitly.
Active never guarantees serving; approval, schedule and
budget also matter. Archived paths cannot be edited.

Never change unselected campaigns, ad groups or ads. When the user explicitly requests
multiple levels, activate ads → groups → campaign (campaign last), or pause
the campaign first. Stop dependent activation on failure; report completed and
remaining targets. Refresh hierarchy snapshots after each successful call before
the next; if relevant state differs beyond those confirmed changes, reconfirm.
Use the same verified/unchanged/rejected/uncertain handling as bidding.

## Images

Use `upload_chatgpt_image` with the selected `org_brand_id`, `account_id` from
live reads and the confirmed public HTTPS image URL. Show the selected image
and confirm before upload; never ask for a local path, API key or terminal step.
The tool prepares a square PNG/JPEG while preserving the image composition,
stores it privately and returns a prepared thumbnail plus an account-bound
`image_ref`. Keep that reference for reuse; do not substitute a raw file ID or
reuse it in another account. Explain any padding/resizing simply.

`uploaded` means the image is ready, not that an ad exists or is running.
For `rejected`, explain only the known failure and ask for a corrected image or
connection when needed. For `uncertain`, say the upload could not be confirmed
or its reference could not be saved; stop dependent work and do not retry
automatically. Separate explicit uploads may create extra image files.
An approved creation plan can include the selected images; do not reconfirm each
upload. Do not promise campaign/ad creation unless its tools are actually available.

## Quick campaign proposals

For a quick one-product campaign with saved context, use `prepare_chatgpt_campaign`. Resolve the
chosen product with `list_brand_products` and pass its exact destination URL,
the customer's goal and any supplied audience/context. Ask only if the product
or intent is unclear. Preparation uses the latest saved Markdown brand knowledge;
if missing, offer the website or console choices in the management skill.
When subscription billing is enabled, a successful proposal uses 10 Mighty credits;
a failed generation releases its reservation. If the customer explicitly asks for
a proposal, briefly state the credit use and proceed. If you suggest generating one,
ask before spending credits. Regenerating a proposal uses another 10 credits; edits
to the returned copy in conversation do not.
For the website choice, draft the proposal directly in chat from the public
evidence and customer input; do not call this saved-context-only tool or invent
source revision IDs. The same separate creation tools work after confirmation.

The tool result is one group, four ads and context hints. Nothing is created, saved as
a campaign draft or launched. Show a compact numbered proposal with product links
and distinct ad angles, plus the selected product image when available; invite
edits in chat. Keep source revision and request
IDs for subsequent calls, without putting them in ordinary customer responses.
The proposal follows brand guidance but is not independent claim verification.

When the customer wants to create it, collect only missing required settings,
confirm the exact plan once, then use the creation tools below. For tool-generated
proposals, reuse each resource's request_id for its first create. For proposals
drafted in chat, assign request UUIDs as described below. Pass the returned campaign
ID to its group, and that group's returned ID to its ads; use the selected
product image through `upload_chatgpt_image`. No local files or review link is
needed. Once a create has been attempted, retain its exact body and request ID;
changes require a new intent, not a retry. Do not regenerate a proposal to recover
an uncertain create. Check the account and retain completed IDs instead.

## Create campaigns, ad groups and ads

Use `create_chatgpt_campaign`, `create_chatgpt_ad_group` and `create_chatgpt_ad`
for one resource each. All create paused; they do not activate other resources.
No local files, terminal, workspace or separate review page is required.
When asked for suggestions, use product fit, brand context and the campaign goal
to propose themes, groupings and distinct ad angles. Explain the choices briefly;
do not impose a fixed group/ad count or invent claims. Let the user refine the plan.

For a new campaign, confirm its name, lifetime budget in the account currency,
objective, schedule and targeting. Do not borrow placeholder budgets or bids
from generated drafts. For an existing campaign, read its current details first.
An ad always needs an ad group. If the user asks to add an ad to a campaign,
show numbered existing groups and offer a new group; ask them to choose.

New groups use fixed bidding: confirm the name, billing type and maximum bid.
Automatic bidding requires the separate bidding-change tool; do not silently
replace it with a fixed bid. Invite optional audience,
product and campaign context once. Draft 15 grounded context hints, including
at least four broad recommendation/category questions; customer-supplied hints
take precedence. Hints are matching guidance, not customer-visible ad copy.
Do not change existing groups' hints. Pass `expected_campaign_updated_at` from
the current campaign details.

For an ad, confirm name, title (3–50 characters), body (1–100 characters),
the exact product/formula destination and prepared image. Use the account's
`image_ref`, never a raw file ID. Pass campaign and ad group IDs and their current
`updated_at` values. Do not invent claims or send a product-specific promise to
an unrelated page. Report creative review in plain language—under review,
approved or rejected—not as proof the ad can run.

Assign a request UUID to each confirmed resource. Retain it with the exact inputs
for that operation; OpenAI receives a stable, brand/account-scoped idempotency key.
A new UUID means a new resource, not a retry. Never automatically repeat an
uncertain create or change its key to bypass a conflict. Check the live account
and stop; an explicitly approved retry must use the original UUID and exact body.
Keep UUIDs and provider timestamps out of ordinary customer responses.

For a full campaign, create campaign → groups → ads within the approved plan.
Give a brief progress update at each stage, not a technical message per call.
Stop dependent work on failure; retain completed IDs and request UUIDs. Resume
only never-attempted, still-approved steps once their dependencies are confirmed.
Do not silently replace a rejected ad, change its copy or expand the plan.

Reuse current campaign/group snapshots while their settings are unchanged; the
server checks them before each create. Do not reread the same campaign before
every independent ad. Refresh on stale-state errors or known external changes.
`confirmation_pending` means OpenAI returned a new ID, but saved details have
not been confirmed yet—not a failed create. Keep the ID and never recreate it.
For a newly accepted group, read its details once. If it is paused and its campaign
does not conflict, use that snapshot to create the still-approved ads; the server
checks its recorded creation even when campaign lists lag. An ID alone is not enough.
If details cannot be confirmed, stop dependent work and offer a status check later.
Use campaign-filtered lists for existing groups. Check the final complete ads
list once per group for counts, copy, images, destinations and paused statuses;
fetch an individual ad only when the list leaves a specific gap. Follow pagination,
but do not loop on pending results or promise background checking. If still pending,
report the remainder and offer to check status later. Do not activate unconfirmed items.

For write outcomes, use the typed status and returned IDs, not a success-sounding
message alone. `provider_error_status_code`, when present, describes a failed write,
not the later confirmation read: 401/403 → check the connection/permissions;
429 → wait and check status; 409 → refresh and reconfirm; other rejected inputs
→ explain the known problem and request a correction. Transport failures and
5xx/408 remain uncertain: check first, never repeat the write automatically.
Credential failures follow the connection/sign-in instructions, never another brand.

Finish with verified counts and a next step: “Created and checked: 1 campaign,
3 groups, 6 ads—all paused. Would you like to review the ads?” On partial completion,
separate confirmed, pending, rejected and not-yet-created items; never call them all
paused or claim zero spend. Existing active campaigns/ads are unchanged and may
keep spending. Activation needs a separate exact-target confirmation, not merely
“continue” or “looks good.” Only offer edits supported by available tools.
