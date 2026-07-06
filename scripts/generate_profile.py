#!/usr/bin/env python3
"""Generate profile metrics SVGs and the 'Recently shipped' README section.

Stdlib only — no pip installs, no third-party stats services. Queries the
GitHub GraphQL API and renders theme-aware SVG panels that match the
header design system, then rewrites the marker-delimited README section.

Usage: GITHUB_TOKEN=... python3 scripts/generate_profile.py
"""

import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER = "copyleftdev"
ROOT = Path(__file__).resolve().parent.parent

QUERY = """
query {
  user(login: "%s") {
    createdAt
    followers { totalCount }
    contributionsCollection { contributionCalendar { totalContributions } }
    allOriginals: repositories(ownerAffiliations: OWNER, isFork: false) {
      totalCount
    }
    repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC,
                 isFork: false, orderBy: {field: PUSHED_AT, direction: DESC}) {
      totalCount
      nodes { name description pushedAt primaryLanguage { name } }
    }
  }
}
""" % USER

# GitHub linguist colors
LANG_COLORS = {
    "Rust": "#dea584",
    "Zig": "#ec915c",
    "Python": "#3572A5",
    "Go": "#00ADD8",
    "Shell": "#89e051",
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "HTML": "#e34c26",
    "Nim": "#ffc200",
    "Assembly": "#6E4C13",
    "C": "#555555",
    "C++": "#f34b7d",
}

THEMES = {
    "dark": dict(bg1="#0d1117", bg2="#161b22", border="#30363d",
                 text="#e6edf3", sub="#8b949e", accent="#58a6ff"),
    "light": dict(bg1="#ffffff", bg2="#f6f8fa", border="#d0d7de",
                  text="#1f2328", sub="#57606a", accent="#0969da"),
}

MONO = "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace"


def fetch(token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY}).encode(),
        headers={"Authorization": f"bearer {token}",
                 "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    if "errors" in data:
        sys.exit(f"GraphQL errors: {data['errors']}")
    return data["data"]["user"]


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_metrics(user, theme):
    t = THEMES[theme]
    contribs = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    followers = user["followers"]["totalCount"]
    repos = user["repositories"]
    originals = repos["totalCount"]
    created = datetime.fromisoformat(user["createdAt"].replace("Z", "+00:00"))
    now = datetime.now(timezone.utc)
    years = now.year - created.year - ((now.month, now.day) < (created.month, created.day))

    # allOriginals includes private repos only when the token can see them;
    # pick the label to match what was actually counted so it can never lie
    all_originals = user["allOriginals"]["totalCount"]
    if all_originals > originals:
        repo_stat = (f"{all_originals:,}", "original repos · incl private")
    else:
        repo_stat = (str(originals), "original public repos")

    stats = [
        (f"{contribs:,}", "contributions · past year"),
        repo_stat,
        (str(years), "years on github"),
        (str(followers), "followers"),
    ]

    langs = {}
    for n in repos["nodes"]:
        lang = (n["primaryLanguage"] or {}).get("name")
        if lang:
            langs[lang] = langs.get(lang, 0) + 1
    total = sum(langs.values())
    top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]
    shown = sum(c for _, c in top)
    segments = [(name, count / total) for name, count in top]
    if total - shown:
        segments.append(("Other", (total - shown) / total))

    parts = [
        f'<svg width="100%" height="210" viewBox="0 0 1200 210" fill="none" xmlns="http://www.w3.org/2000/svg">',
        '<defs>',
        f'<linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">'
        f'<stop offset="0%" style="stop-color:{t["bg1"]}"/>'
        f'<stop offset="100%" style="stop-color:{t["bg2"]}"/></linearGradient>',
        '<clipPath id="bar"><rect x="100" y="148" width="1000" height="8" rx="4"/></clipPath>',
        '</defs>',
        f'<rect x="0.5" y="0.5" width="1199" height="209" rx="6" fill="url(#bg)" stroke="{t["border"]}"/>',
        f'<text x="100" y="42" fill="{t["sub"]}" font-family="{MONO}" font-size="12" letter-spacing="3">'
        f'LIVE TELEMETRY <tspan fill="{t["accent"]}">//</tspan> regenerated nightly from the GitHub API</text>',
    ]

    x = 100
    for value, label in stats:
        parts.append(
            f'<text x="{x}" y="100" fill="{t["text"]}" font-family="{MONO}" '
            f'font-size="34" font-weight="700">{value}</text>')
        parts.append(
            f'<text x="{x}" y="122" fill="{t["sub"]}" font-family="{MONO}" '
            f'font-size="11" letter-spacing="2">{esc(label.upper())}</text>')
        x += 275

    # language bar
    bx = 100.0
    for name, frac in segments:
        w = frac * 1000
        color = LANG_COLORS.get(name, t["sub"])
        parts.append(
            f'<rect x="{bx:.1f}" y="148" width="{w:.1f}" height="8" '
            f'fill="{color}" clip-path="url(#bar)"/>')
        bx += w

    lx = 100
    for name, frac in segments:
        color = LANG_COLORS.get(name, t["sub"])
        label = f"{name} {frac * 100:.0f}%"
        parts.append(f'<circle cx="{lx + 4}" cy="178" r="4" fill="{color}"/>')
        parts.append(
            f'<text x="{lx + 14}" y="182" fill="{t["sub"]}" '
            f'font-family="{MONO}" font-size="12">{esc(label)}</text>')
        lx += 14 + int(len(label) * 7.3) + 26

    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def truncate(desc, limit=96):
    desc = " ".join((desc or "—").split())
    if len(desc) <= limit:
        return desc
    return desc[: limit - 1].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def render_recent(user, count=6):
    rows = [
        "| Repository | Description | Lang | Last push |",
        "|:-----------|:------------|:----:|:----------|",
    ]
    nodes = [n for n in user["repositories"]["nodes"] if n["name"] != USER]
    for n in nodes[:count]:
        lang = (n["primaryLanguage"] or {}).get("name") or "—"
        desc = truncate(n["description"]).replace("|", "\\|")
        pushed = n["pushedAt"][:10]
        rows.append(
            f"| [{n['name']}](https://github.com/{USER}/{n['name']}) "
            f"| {desc} | $\\texttt{{{lang}}}$ | {pushed} |")
    return "\n".join(rows)


def update_readme(section):
    path = ROOT / "README.md"
    text = path.read_text()
    block = f"<!--RECENT:START-->\n{section}\n<!--RECENT:END-->"
    new = re.sub(r"<!--RECENT:START-->.*?<!--RECENT:END-->", lambda _: block,
                 text, flags=re.S)
    if "<!--RECENT:START-->" not in new:
        sys.exit("README.md is missing the RECENT markers")
    path.write_text(new)


def main():
    token = os.environ.get("METRICS_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("METRICS_TOKEN or GITHUB_TOKEN is required")
    user = fetch(token)
    (ROOT / "assets" / "metrics.svg").write_text(render_metrics(user, "dark"))
    (ROOT / "assets" / "metrics-light.svg").write_text(render_metrics(user, "light"))
    update_readme(render_recent(user))
    print("regenerated: assets/metrics.svg, assets/metrics-light.svg, README recent section")


if __name__ == "__main__":
    main()
