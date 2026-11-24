# Mighty Ads plugins

Mighty Ads Agent helps merchants review and optimize Meta Ads, Google Ads and
ChatGPT Ads through focused workflows, and manage supported ad settings in
MightyAI. The Claude plugin lives in [`claude/`](claude/); see its
[README](claude/README.md) for what it does, the data it accesses and how to
get support.

## Install in Claude Code

```
/plugin install mighty-ads --marketplace oski-labs/mighty-ads-plugins
```

After installing, run `/mcp` and sign in to MightyAI, then choose the
workspace you want to use.

## License

Proprietary. See [`claude/LICENSE`](claude/LICENSE).

<!-- mighty-ads:downloads:start -->
## Install and download

### Claude Code

```sh
/plugin install mighty-ads --marketplace oski-labs/mighty-ads-plugins
```

After installing, run `/mcp` and sign in to MightyAI.
[Download Claude ZIP](https://plugins.getmighty.ai/mighty-ads/0.1.34/mighty-ads-claude-0.1.34-g4abbe9f6af72.zip).

### Codex

[Download the Codex marketplace ZIP](https://plugins.getmighty.ai/mighty-ads/0.1.34/mighty-ads-chatgpt-0.1.34-g4abbe9f6af72.zip) and extract it,
including the hidden `.agents` folder, into a persistent directory. Register the
extracted directory and install the plugin:

```sh
codex plugin marketplace add /absolute/path/to/extracted-marketplace
codex plugin add mighty-ads@mighty-repo
```

Connect Mighty Ads through Codex plugin settings and select your Mighty workspace.
The marketplace files are also available at this repository's root.

### ChatGPT / OpenAI plugin submission

[Download the single-plugin upload ZIP](https://plugins.getmighty.ai/mighty-ads/0.1.34/mighty-ads-0.1.34-g4abbe9f6af72-plugin.zip).
This archive has `plugin.json` at its root and is the OpenAI portal upload format.
The Codex ZIP retains a historical `chatgpt` filename but is a different format.
Publishing these files does not publish or update a ChatGPT listing; portal
submission and approval are separate.

Release **0.1.34**, source commit `4abbe9f6af72ec50c4b0d03706f33c66f35c5484`.
[Release manifest](https://plugins.getmighty.ai/mighty-ads/0.1.34/release.json) · [Checksums](https://plugins.getmighty.ai/mighty-ads/0.1.34/SHA256SUMS.txt).
<!-- mighty-ads:downloads:end -->
