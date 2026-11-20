"""Verify and export public Mighty Ads releases (stdlib-only public-repo helper)."""

import argparse
import base64
import json
import re
import stat
import subprocess
import sys
from functools import cache
from hashlib import sha256
from io import BytesIO
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from typing import Any
from urllib.request import Request, urlopen
from zipfile import ZipFile

ORIGIN = "https://plugins.getmighty.ai"
REPOSITORY = "oski-labs/mighty-ads-plugins"
VERSION = re.compile(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)")
START = "<!-- mighty-ads:downloads:start -->"
END = "<!-- mighty-ads:downloads:end -->"
STATE = ".public-plugin-files.json"
SKILLS = (
    "find-wasted-ad-spend",
    "google-search-query-optimizer",
    "inspect-brand-knowledge",
    "manage-ads",
    "meta-audience-placements",
    "meta-creative-health",
    "meta-customer-dropoffs",
    "setup",
    "start-with-mighty-ads",
    "weekly-ads-review",
)
REFERENCES = (
    "amazon-ads",
    "chatgpt-ads",
    "google-ads",
    "meta-ads",
    "microsoft-ads",
    "reddit-ads",
    "snapchat-ads",
    "tiktok-ads",
    "x-ads",
)
COMMON = {
    "README.md",
    "LICENSE",
    "assets/logo.png",
    *(f"skills/{skill}/SKILL.md" for skill in SKILLS),
    *(f"skills/manage-ads/references/{name}.md" for name in REFERENCES),
    "skills/references/ads-analysis-principles.md",
    "skills/references/workflow-response-pattern.md",
}
CLAUDE = COMMON | {".claude-plugin/plugin.json", ".mcp.json"}
OPENAI = COMMON | {"plugin.json", "mcp.json"}
# OpenAI packages carry skill-local copies of these known supporting documents.
OPENAI |= {
    f"skills/{skill}/references/{name}.md"
    for skill in SKILLS
    for name in (*REFERENCES, "ads-analysis-principles", "workflow-response-pattern")
}
CODEX = {
    ".agents/plugins/marketplace.json",
    "README.md",
    "client-support.json",
    *(f"plugins/mighty-ads/{name}" for name in OPENAI),
}
PUBLIC_PATHS = {
    *(f"claude/{name}" for name in CLAUDE),
    *(name for name in CODEX if name != "README.md"),
    ".claude-plugin/marketplace.json",
    "release.json",
}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def read_https(url: str) -> bytes:
    if not url.startswith(f"{ORIGIN}/mighty-ads/"):
        raise ValueError("Download must use the approved public release origin")
    request = Request(url, headers={"user-agent": "Mighty-Ads-public-sync"})  # noqa: S310
    with urlopen(request, timeout=30) as response:  # noqa: S310
        if not response.url.startswith(f"{ORIGIN}/mighty-ads/"):
            raise ValueError("Download redirected outside public release origin")
        data = response.read(10 * 1024 * 1024 + 1)
    if len(data) > 10 * 1024 * 1024:
        raise ValueError("Release file exceeds size limit")
    return data


def version_key(version: str) -> tuple[int, ...]:
    if not VERSION.fullmatch(version):
        raise ValueError("Expected a stable release version")
    return tuple(map(int, version.split(".")))


def verified_release(
    manifest: dict[str, Any], *, read: Any = read_https
) -> dict[str, bytes]:
    """Check identity, canonical URLs and hashes before consuming any package."""
    version_key(manifest["version"])
    commit = manifest["commit"]
    if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Invalid release source commit")
    if manifest.get("schema_version") != 1 or set(manifest) != {
        "schema_version",
        "version",
        "commit",
        "packages",
        "release_url",
        "checksums_url",
    }:
        raise ValueError("Invalid public release manifest")
    packages = manifest["packages"]
    if set(packages) not in (
        {"claude", "codex", "openai"},
        {"claude", "codex", "openai", "gemini", "antigravity"},
    ):
        raise ValueError("Unsupported release package set")
    prefix = f"{ORIGIN}/mighty-ads/{manifest['version']}"
    for field, filename in [
        ("release_url", "release.json"),
        ("checksums_url", "SHA256SUMS.txt"),
    ]:
        if manifest[field] != f"{prefix}/{filename}":
            raise ValueError("Invalid public release URL")
    manifest_bytes = read(manifest["release_url"])
    if json.loads(manifest_bytes) != manifest:
        raise ValueError("Public release manifest differs from requested release")
    files = {"release.json": manifest_bytes}
    checksums = []
    for client in ("claude", "codex", "gemini", "antigravity", "openai"):
        if client not in packages:
            continue
        package = packages[client]
        label = "chatgpt" if client == "codex" else client
        name = (
            f"mighty-ads-{manifest['version']}-g{commit[:12]}-plugin.zip"
            if client == "openai"
            else f"mighty-ads-{label}-{manifest['version']}-g{commit[:12]}.zip"
        )
        if set(package) != {"filename", "sha256", "size", "url"} or (
            package["filename"] != name
            or package["url"] != f"{prefix}/{name}"
            or not re.fullmatch(r"[0-9a-f]{64}", package["sha256"])
            or type(package["size"]) is not int
            or not 0 < package["size"] <= 10 * 1024 * 1024
        ):
            raise ValueError("Invalid release package identity")
        data = read(package["url"])
        if (
            len(data) != package["size"]
            or sha256(data).hexdigest() != package["sha256"]
        ):
            raise ValueError("Release package checksum or size mismatch")
        files[name] = data
        checksums.append(f"{package['sha256']}  {name}\n")
    sums = read(manifest["checksums_url"])
    if sums != "".join(checksums).encode():
        raise ValueError("Release checksums file mismatch")
    files["SHA256SUMS.txt"] = sums
    return files


def unpack(data: bytes, client: str, version: str) -> dict[str, bytes]:
    allowed = {"claude": CLAUDE, "codex": CODEX, "openai": OPENAI}[client]
    wrapper = (
        ""
        if client == "openai"
        else f"mighty-ads-{'chatgpt' if client == 'codex' else client}-{version}/"
    )
    files: dict[str, bytes] = {}
    with ZipFile(BytesIO(data)) as archive:
        if sum(item.file_size for item in archive.infolist()) > 20 * 1024 * 1024:
            raise ValueError("Expanded package exceeds size limit")
        for entry in archive.infolist():
            name = entry.filename
            mode = entry.external_attr >> 16
            if (
                not name.startswith(wrapper)
                or entry.is_dir()
                or stat.S_IFMT(mode) not in {0, stat.S_IFREG}
            ):
                raise ValueError("Unsafe ZIP entry")
            name = name.removeprefix(wrapper)
            if name not in allowed or name in files or not entry.file_size:
                raise ValueError("Unexpected, duplicate or empty package file")
            files[name] = archive.read(entry)
    required = {
        "claude": {
            ".claude-plugin/plugin.json",
            ".mcp.json",
            "README.md",
            "LICENSE",
            "assets/logo.png",
        },
        "codex": {
            ".agents/plugins/marketplace.json",
            "client-support.json",
            "plugins/mighty-ads/plugin.json",
            "plugins/mighty-ads/mcp.json",
        },
        "openai": {
            "plugin.json",
            "mcp.json",
            "README.md",
            "LICENSE",
            "assets/logo.png",
        },
    }[client]
    required |= {
        f"{'plugins/mighty-ads/' if client == 'codex' else ''}skills/{skill}/SKILL.md"
        for skill in SKILLS
    }
    if not required <= files.keys():
        raise ValueError("Package is missing required files")
    manifest_name = {
        "claude": ".claude-plugin/plugin.json",
        "codex": "plugins/mighty-ads/plugin.json",
        "openai": "plugin.json",
    }[client]
    manifest = json.loads(files[manifest_name])
    if manifest.get("name") != "mighty-ads" or manifest.get("version") != version:
        raise ValueError("Packaged plugin version or name mismatch")
    mcp_name = {
        "claude": ".mcp.json",
        "codex": "plugins/mighty-ads/mcp.json",
        "openai": "mcp.json",
    }[client]
    if json.loads(files[mcp_name]).get("mcpServers") != {
        "mighty": {
            "type": "http" if client == "claude" else "streamable-http",
            "url": "https://api.mightyai.app/mcp",
        },
    }:
        raise ValueError("Package must use production MCP without embedded credentials")
    if client == "codex":
        catalog = json.loads(files[".agents/plugins/marketplace.json"])
        if (
            catalog.get("name") != "mighty-repo"
            or catalog.get("plugins")
            != [
                {
                    "name": "mighty-ads",
                    "source": {"source": "local", "path": "./plugins/mighty-ads"},
                    "policy": {
                        "installation": "AVAILABLE",
                        "authentication": "ON_INSTALL",
                    },
                    "category": "Productivity",
                }
            ]
            or json.loads(files["client-support.json"]).get("release") != version
        ):
            raise ValueError("Codex marketplace or support version mismatch")
    return files


def downloads_section(manifest: dict[str, Any]) -> str:
    packages = manifest["packages"]
    return f"""{START}
## Install and download

### Claude Code

```sh
/plugin install mighty-ads --marketplace {REPOSITORY}
```

After installing, run `/mcp` and sign in to MightyAI.
[Download Claude ZIP]({packages["claude"]["url"]}).

### Codex

[Download the Codex marketplace ZIP]({packages["codex"]["url"]}) and extract it,
including the hidden `.agents` folder, into a persistent directory. Register the
extracted directory and install the plugin:

```sh
codex plugin marketplace add /absolute/path/to/extracted-marketplace
codex plugin add mighty-ads@mighty-repo
```

Connect Mighty Ads through Codex plugin settings and select your Mighty workspace.
The marketplace files are also available at this repository's root.

### ChatGPT / OpenAI plugin submission

[Download the single-plugin upload ZIP]({packages["openai"]["url"]}).
This archive has `plugin.json` at its root and is the OpenAI portal upload format.
The Codex ZIP retains a historical `chatgpt` filename but is a different format.
Publishing these files does not publish or update a ChatGPT listing; portal
submission and approval are separate.

Release **{manifest["version"]}**, source commit `{manifest["commit"]}`.
[Release manifest]({manifest["release_url"]}) · [Checksums]({manifest["checksums_url"]}).
{END}"""


def safe_path(root: Path, name: str) -> Path:
    path = PurePosixPath(name)
    if path.is_absolute() or ".." in path.parts or "\\" in name:
        raise ValueError("Unsafe managed path")
    result = root / name
    chain = [root.joinpath(*path.parts[:index]) for index in range(len(path.parts) + 1)]
    if any(part.is_symlink() for part in chain):
        raise ValueError("Public destination must not contain symlinks")
    return result


def check_order(previous: dict[str, Any] | None, manifest: dict[str, Any]) -> None:
    if previous is None:
        return
    old, new = version_key(previous["version"]), version_key(manifest["version"])
    if old > new:
        raise ValueError("Refusing an older public release")
    if old == new and previous != manifest:
        raise ValueError("Refusing conflicting content for an existing release version")


def export_release(
    manifest: dict[str, Any], root: Path, *, read: Any = read_https
) -> dict[str, bytes]:
    """Validate everything before writing; manage only declared public paths."""
    read = cache(read)
    payloads = verified_release(manifest, read=read)
    clients = {
        client: unpack(
            payloads[manifest["packages"][client]["filename"]],
            client,
            manifest["version"],
        )
        for client in ("claude", "codex", "openai")
    }
    # OpenAI is the exact canonical plugin subtree, not a separately edited copy.
    if clients["openai"] != {
        name.removeprefix("plugins/mighty-ads/"): data
        for name, data in clients["codex"].items()
        if name.startswith("plugins/mighty-ads/")
    }:
        raise ValueError("Codex and OpenAI plugin contents differ")
    result = {f"claude/{name}": data for name, data in clients["claude"].items()}
    result.update(
        {name: data for name, data in clients["codex"].items() if name != "README.md"}
    )
    catalog_path = safe_path(root, ".claude-plugin/marketplace.json")
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_bytes())
        entries = [
            item
            for item in catalog.get("plugins", [])
            if item.get("name") == "mighty-ads"
        ]
        if (
            catalog.get("name") != "mighty-ads-plugins"
            or len(entries) != 1
            or entries[0].get("source") != "./claude"
        ):
            raise ValueError("Existing Claude marketplace identity must be preserved")
    else:
        catalog = {
            "name": "mighty-ads-plugins",
            "owner": {"name": "MightyAI"},
            "plugins": [{"name": "mighty-ads", "source": "./claude"}],
        }
    result[".claude-plugin/marketplace.json"] = json_bytes(catalog)
    result["release.json"] = payloads["release.json"]
    provenance = safe_path(root, "release.json")
    check_order(
        json.loads(provenance.read_bytes()) if provenance.exists() else None, manifest
    )
    state = safe_path(root, STATE)
    old = set(json.loads(state.read_bytes())) if state.exists() else set()
    if not old <= PUBLIC_PATHS:
        raise ValueError("Invalid managed file ownership list")
    result[STATE] = json_bytes(sorted(result))
    readme = safe_path(root, "README.md")
    text = readme.read_text() if readme.exists() else "# Mighty Ads plugins\n"
    if START in text or END in text:
        if (
            text.count(START) != 1
            or text.count(END) != 1
            or text.index(START) > text.index(END)
        ):
            raise ValueError("Invalid managed README section")
        text = (
            text[: text.index(START)]
            + downloads_section(manifest)
            + text[text.index(END) + len(END) :]
        )
    else:
        text = text.rstrip() + "\n\n" + downloads_section(manifest) + "\n"
    result["README.md"] = text.encode()
    for name in old | result.keys():
        safe_path(root, name)
    for name in old - result.keys():
        safe_path(root, name).unlink(missing_ok=True)
    for name, data in result.items():
        path = safe_path(root, name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return result


def validate_tree(
    root: Path, *, previous: dict[str, Any] | None = None, read: Any = read_https
) -> dict[str, bytes]:
    read = cache(read)
    manifest = json.loads(safe_path(root, "release.json").read_bytes())
    check_order(previous, manifest)
    with TemporaryDirectory(prefix="mighty-public-verify-") as temp:
        expected = Path(temp)
        expected.mkdir(exist_ok=True)
        for name in ("README.md", ".claude-plugin/marketplace.json"):
            source = safe_path(root, name)
            destination = expected / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(source.read_bytes())
        files = export_release(manifest, expected, read=read)
        for name, data in files.items():
            if safe_path(root, name).read_bytes() != data:
                raise ValueError(f"Public file differs from verified release: {name}")
        for prefix in ("claude", "plugins/mighty-ads", ".agents", ".claude-plugin"):
            for path in (root / prefix).rglob("*"):
                name = path.relative_to(root).as_posix()
                safe_path(root, name)
                if path.is_file() and name not in files:
                    raise ValueError(f"Unmanaged file in plugin tree: {name}")
    return verified_release(manifest, read=read)


class GitHub:
    """Use gh's authenticated transport; never print its error bodies or tokens."""

    def __init__(self, repository: str = REPOSITORY):
        if repository != REPOSITORY:
            raise ValueError("Unexpected public repository")
        self.repository = repository

    def call(self, method: str, path: str, body: Any = None) -> Any:
        command = ["gh", "api", "--method", method, f"repos/{self.repository}/{path}"]
        if body is not None:
            command += ["--input", "-"]
        result = subprocess.run(  # noqa: S603
            command,
            input=json.dumps(body) if body is not None else None,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(
                f"GitHub {method} request failed; inspect permissions and remote state"
            )
        response = json.loads(result.stdout) if result.stdout else None
        if (
            method == "GET"
            and isinstance(response, list)
            and len(response) == 100
            and "per_page=100" in path
            and "&page=" not in path
        ):
            page = 2
            while True:
                following = self.call("GET", f"{path}&page={page}")
                response.extend(following)
                if len(following) < 100:
                    break
                page += 1
        return response

    def upload(self, release_id: int, path: Path) -> None:
        result = subprocess.run(  # noqa: S603
            [  # noqa: S607
                "gh",
                "api",
                "--method",
                "POST",
                f"https://uploads.github.com/repos/{self.repository}/releases/{release_id}/assets?name={path.name}",
                "--header",
                "content-type: application/octet-stream",
                "--input",
                str(path),
            ],
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise RuntimeError("GitHub asset upload failed; rerun to reconcile")


def git_tree(github: Any, commit: str) -> tuple[str, dict[str, dict[str, str]]]:
    tree_sha = github.call("GET", f"git/commits/{commit}")["tree"]["sha"]
    response = github.call("GET", f"git/trees/{tree_sha}?recursive=1")
    if response.get("truncated"):
        raise ValueError("Public repository tree is truncated")
    return tree_sha, {
        item["path"]: item for item in response["tree"] if item["type"] != "tree"
    }


def resolve_tag_commit(github: Any, target: dict[str, str]) -> str:
    """Resolve lightweight or annotated Git tags to a commit."""
    seen: set[str] = set()
    while True:
        sha = target["sha"]
        if not re.fullmatch(r"[0-9a-f]{40}", sha) or sha in seen:
            raise ValueError("Existing release tag has an invalid target")
        if target["type"] == "commit":
            return sha
        if target["type"] != "tag":
            raise ValueError("Existing release tag must point to a commit")
        seen.add(sha)
        target = github.call("GET", f"git/tags/{sha}")["object"]


def validate_remote_tree(
    github: Any, commit: str, manifest: dict[str, Any], *, read: Any
) -> None:
    """An existing tag/draft must identify a valid installation tree too."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Existing release has an unexpected target")
    _, nodes = git_tree(github, commit)
    with TemporaryDirectory(prefix="mighty-existing-tag-") as temp:
        root = Path(temp)
        for name, node in nodes.items():
            if name not in PUBLIC_PATHS | {STATE, "README.md"}:
                if name.startswith(
                    ("claude/", "plugins/mighty-ads/", ".agents/", ".claude-plugin/")
                ):
                    raise ValueError("Unmanaged file in existing release tree")
                continue
            if node["mode"] != "100644" or node["type"] != "blob":
                raise ValueError("Existing release tree contains a non-regular file")
            blob = github.call("GET", f"git/blobs/{node['sha']}")
            path = safe_path(root, name)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(base64.b64decode(blob["content"]))
        if json.loads((root / "release.json").read_bytes()) != manifest:
            raise ValueError("Existing release tree has conflicting provenance")
        validate_tree(root, read=read)


def publish_github(
    root: Path, commit: str, *, github: Any = None, read: Any = read_https
) -> None:
    github = github or GitHub()
    files = validate_tree(root, read=read)
    manifest = json.loads(files["release.json"])
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Expected full public merge SHA")
    # Serialize the public workflow and refuse an outdated checkout on every run.
    if github.call("GET", "git/ref/heads/main")["object"]["sha"] != commit:
        raise ValueError("Public main advanced; rerun publication from current main")
    version = manifest["version"]
    tag = f"v{version}"
    refs = github.call("GET", f"git/matching-refs/tags/{tag}")
    matching = [item for item in refs if item["ref"] == f"refs/tags/{tag}"]
    if matching:
        tagged_commit = resolve_tag_commit(github, matching[0]["object"])
        if tagged_commit != commit:
            validate_remote_tree(github, tagged_commit, manifest, read=read)
    releases = github.call("GET", "releases?per_page=100")
    newer = any(
        VERSION.fullmatch(item["tag_name"].removeprefix("v"))
        and version_key(item["tag_name"].removeprefix("v")) > version_key(version)
        for item in releases
        if not item["draft"] and not item["prerelease"]
    )
    if newer:
        raise ValueError(
            "Refusing to promote a release older than GitHub's published releases"
        )
    existing = next((item for item in releases if item["tag_name"] == tag), None)
    if existing is None:
        existing = github.call(
            "POST",
            "releases",
            {
                "tag_name": tag,
                "target_commitish": commit,
                "name": f"Mighty Ads {version}",
                "body": f"Verified packages from {manifest['release_url']}",
                "draft": True,
                "make_latest": "false",
            },
        )
    if not matching and existing.get("target_commitish") != commit:
        validate_remote_tree(
            github, existing.get("target_commitish", ""), manifest, read=read
        )
    if existing.get("prerelease"):
        raise ValueError("Existing release is unexpectedly a prerelease")
    assets = github.call("GET", f"releases/{existing['id']}/assets?per_page=100")
    with TemporaryDirectory(prefix="mighty-assets-") as temp:
        for name, data in files.items():
            asset = next((item for item in assets if item["name"] == name), None)
            if (
                asset is not None
                and existing["draft"]
                and asset.get("state") == "starter"
                and asset.get("size") == 0
            ):
                github.call("DELETE", f"releases/assets/{asset['id']}")
                asset = None
            if asset is not None:
                if (
                    asset.get("state") != "uploaded"
                    or asset.get("size") != len(data)
                    or asset.get("digest") != f"sha256:{sha256(data).hexdigest()}"
                ):
                    raise ValueError(
                        "Existing GitHub release asset differs; refusing overwrite"
                    )
            else:
                if not existing["draft"]:
                    raise ValueError(
                        "Published release is incomplete; refusing to mutate it"
                    )
                path = Path(temp) / name
                path.write_bytes(data)
                github.upload(existing["id"], path)
        # Read back server checksums before making a draft visible.
        uploaded = github.call("GET", f"releases/{existing['id']}/assets?per_page=100")
        if {asset["name"] for asset in uploaded} != set(files) or any(
            asset.get("state") != "uploaded"
            or asset.get("size") != len(files[asset["name"]])
            or asset.get("digest")
            != f"sha256:{sha256(files[asset['name']]).hexdigest()}"
            for asset in uploaded
        ):
            raise ValueError("GitHub release assets did not verify")
    if existing["draft"]:
        # Asset uploads may outlast the checkout's selection on main.
        if github.call("GET", "git/ref/heads/main")["object"]["sha"] != commit:
            raise ValueError(
                "Public main advanced; rerun publication from current main"
            )
        github.call(
            "PATCH",
            f"releases/{existing['id']}",
            {"draft": False, "make_latest": "true"},
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("validate", "publish"))
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base", type=Path)
    parser.add_argument("--commit")
    args = parser.parse_args()
    try:
        previous = (
            json.loads((args.base / "release.json").read_bytes())
            if args.base and (args.base / "release.json").exists()
            else None
        )
        validate_tree(args.root, previous=previous)
        if args.command == "publish":
            if not args.commit:
                raise ValueError("Publication requires --commit")
            publish_github(args.root, args.commit)
        print(
            "Public release verified"
            if args.command == "validate"
            else "GitHub release verified and published"
        )
        return 0
    except (ValueError, TypeError, KeyError, OSError, RuntimeError):
        print(
            "Public release failed; check release identity, package integrity, permissions and remote state.",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
