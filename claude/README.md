# Mighty Ads

Review Meta Ads, Google Search and ChatGPT Ads in your AI assistant using ten
focused skills.
Ask for a weekly performance review, wasted-spend analysis, Google Search query
recommendations, or Meta creative, audience and customer drop-off analysis.
Results depend on your connected accounts and available reporting data.

## Connect your account

Install the Mighty Ads plugin, enable its `mighty` connection and complete browser
sign-in with your own Mighty account. Choose the workspace containing your brands.
The connection uses the hosted service at https://api.mightyai.app/mcp. Ask your
assistant to list your brands and confirm the intended brand before requesting a
report. Advertising accounts must be connected in Mighty; installing the plugin
does not connect an advertiser account or establish conversion measurement
readiness.

To use a different workspace, reconnect `mighty` in your assistant's connection
settings and select that workspace during sign-in. The plugin's setup skill
covers the steps for each supported assistant.

## Try a workflow

- “Show the advertising tasks available for my brand. Do not make changes.”
- “Review my ads for the last seven complete days and explain missing data.”
- “Which Google Search queries should I investigate?”
- “What saved brand guidance does Mighty have for my brand?”

Supported tools can also prepare paused campaigns and change supported advertising
settings. Review the brand, advertiser, scope and exact proposed changes before
approving an action. Activation can enable real advertising spend. Missing reports
are not zero results, and provider conversions are distinct from Shopify-attributed
orders. Support varies by channel; the plugin does not provide every advertiser
setting or operation.

## Connections and data handling

This package contains instructions, references, branding and remote MCP
configuration. It bundles no local server, executable scripts, account credentials
or advertising records. Your assistant sends tool arguments, such as brand
identifiers, reporting dates and approved advertising settings, to Mighty. The
hosted service uses your authorized workspace and connected providers to retrieve
information or perform supported actions, and returns results to your assistant.
Saved brand guidance and advertising information returned by tools are therefore
processed by your assistant's provider.
Mighty retains tool-call audit information; disconnecting does not delete historical
records or pause campaigns. Never paste passwords, API keys or tokens into chat.

See the [privacy policy](https://www.getmighty.ai/privacy) and
[terms](https://www.getmighty.ai/terms). For account, privacy or deletion questions,
use [Mighty support](https://www.getmighty.ai/contact).
