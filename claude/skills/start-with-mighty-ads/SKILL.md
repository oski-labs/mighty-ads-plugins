---
name: start-with-mighty-ads
description: Show a connection-aware Mighty Ads starting menu when a merchant asks what they can do, where to begin, for help getting started, or which advertising workflows are available.
---

# Start with Mighty Ads

Read [the response pattern](../references/workflow-response-pattern.md). This is a
short router, not an account audit.

Resolve the requested or selected brand with `list_organization_brands`, following
[the setup skill's](../setup/SKILL.md) brand and workspace boundaries. After
resolving one brand, run lightweight `check_google_ads_readiness`,
`check_meta_ads_readiness` and `check_chatgpt_ads_readiness` checks. These reads
need no confirmation and may run in parallel. A failed check means availability
is unknown unless its message explicitly says that channel must be connected;
that is a confirmed unavailable channel. For ChatGPT Ads, working advertiser
reads can support read workflows even when launch measurement is incomplete;
mention that limitation only when it affects the selected work. Do not inspect
campaigns or performance merely to build the menu.

Show two compact numbered sections using only choices relevant to this brand:

**Available now**

- Any connected channel: review performance or find wasted spend.
- Meta: check creative health, find funnel drop-offs, or improve audiences and
  placements; these analyses change nothing. Offer paused photo creation and
  supported campaign, ad set and ad changes only when the selected Meta
  connection reports `management_permission_granted=true`. If false or unknown,
  keep analysis available and direct merchants who need changes to management
  authorization in Integrations. Each change still needs its own approval.
- Google: optimize search queries and keywords, or create and manage supported
  Search campaigns.
- ChatGPT Ads: create or manage campaigns, ads, bids and delivery settings.

Combine overlapping choices instead of listing the same workflow per channel.
Keep the initial menu to at most seven choices. Name connected channels beside a
cross-channel choice when that prevents ambiguity.

**Connect more channels**

List supported but unavailable channels and what each unlocks in one short line.
Offer the brand's Integrations flow in
[Mighty Console](https://console.mightyai.app); never request credentials in chat.
Do not call a channel disconnected when its readiness check failed temporarily.

If no brand is available or the requested brand is missing, follow the setup
skill instead of showing a misleading capability menu. If several brands match,
ask for a numbered choice before checking channels.

Keep numbering stable for the displayed menu. Accept a number, several numbers or
the workflow name. Begin the selected workflow immediately; do not repeat or
explain the menu again. For a connection choice, guide setup and then offer the
newly available next actions.
