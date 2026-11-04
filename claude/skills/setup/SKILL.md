---
name: setup-mighty-ads
description: Help a user connect Mighty Ads to the Clerk workspace they choose, identify multiple connected workspaces, and check advertiser and measurement readiness before launch.
---

# Set up Mighty Ads

Connect Mighty through your host's MCP connection flow and complete Clerk sign-in.
In Codex, use the plugin's account settings; in Claude Code, use its MCP sign-in flow.
The organization chosen there is the connection's authorization boundary. Discover
its brands with `list_organization_brands`; never request organization IDs, brand
IDs, provider keys, tokens or OTPs in chat.

When the host exposes multiple existing Mighty connections, choose the one whose
reliable connection label matches the requested workspace, or ask the user to
select the intended connection in the host. If the labels do not distinguish
workspaces, ask rather than guessing. Discover brands afresh using that connection;
never reuse brand IDs or selections from another connection. Selecting an existing
connection does not expand its authorization to another organization.

Match a brand named in the request against the returned brands. For a unique
match, select it for reads and state which brand is being used. An explicit new
brand replaces the previous selection in this conversation. If the requested
brand is absent, use the unavailable-brand handling below and never substitute
the sole available brand. When no brand is specified, retain the conversation's
selected brand only if it is available in this connection. Default to the sole
available brand only when there is no existing selection to resolve. For duplicate
names or a request such as "switch brands" with several possible targets, show
numbered choices and ask. Never infer a brand from another conversation. An empty list means no available brands;
a failed discovery does not mean an empty list.

Switch between brands within this organization without signing in again. Reuse
the selected brand's exact `org_brand_id` in subsequent calls. On a brand change,
discard previous campaign, ad group, ad, product and provider-account selections
and read the new brand's data afresh. Do not claim the switch succeeded until the
brand is resolved from the accessible list. There is no shared active-brand
setting: switching in one chat must not change another chat's target.

Keep the selected brand when changing advertising channels. ChatGPT, Google and
Meta each require their own connection for that brand. Check the requested
channel's readiness and select a provider account when necessary. Never reuse a
Google or Meta account from the previous brand. For a cross-channel performance
request, check each requested channel separately and report unavailable channels
explicitly. A request for ChatGPT performance alone does not require extra calls
to Google or Meta. Connection readiness does not prove a performance report works.

Switching brands or channels does not authorize ad changes. Before writing,
show the exact brand, advertiser, resources, proposed change and delivery/spend
impact, then obtain confirmation for that unchanged plan. Never carry a write
approval across brands.

If the requested brand is absent, explain that it is unavailable in the current
connection's organization; do not silently select another brand. Check existing
host connections using the labels or workspace choice described above. If the
intended workspace already has a usable connection, select it or ask the user to
select it, then discover its brands before continuing. Clear the prior brand,
campaign, product and provider-account selections and write approvals when the
connection changes. Suggest Add account or reconnect through Clerk only when no
usable connection exists for the requested workspace or login. Do not initiate
broader organization consent or claim that a tool can switch a connection's
organization.

When the user asks whether ChatGPT Ads is ready to launch, use
`check_chatgpt_ads_readiness` for the selected brand. Explain the account and
measurement states separately, then relay the returned next steps. A saved key
or configured Pixel is not proof of working access or conversion measurement.
If either check is incomplete or temporarily unverifiable, do not call the
brand ready. Direct the user to the existing Integrations setup or reconnect
flow; never ask them to paste a credential into chat. A ready result confirms
current advertiser access and required measurement configuration, not an
observed end-to-end conversion or delivery by a particular campaign.

For Google Ads, use `check_google_ads_readiness` for the selected brand. It
verifies account read access only—not campaign access, tracking, launch readiness
or permission to make changes. Search writes validate the approved request with
Google before submission; read readiness alone is not write readiness. If a connection
is missing or access was revoked, direct the user to that brand's Google Ads
integration; never request tokens or credentials in chat.

For Meta Ads, use `check_meta_ads_readiness` to find the selected brand's saved
connections. Ask the user to choose by account name if several exist, then reuse
that connection ID. Account access does not verify Pixel/CAPI or launch readiness.
Direct missing or revoked grants to the existing Meta integration. Meta creation
and edits also require saved management access: check it with
`check_meta_ads_creation_readiness` or `get_meta_edit_context` before proposing a
change. Read access is never elevated by a change request.
