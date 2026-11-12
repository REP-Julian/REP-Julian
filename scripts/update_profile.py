#!/usr/bin/env python3
"""
Autonomous Profile Telemetry & Repository Synchronizer
Author: Julian Agustino (@REP-Julian)
Runs on GitHub Actions schedule + repository events.
"""

import os
import re
import json
import urllib.request
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

GITHUB_USER = "REP-Julian"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

GRAPHQL_URL = "https://api.github.com/graphql"
REST_USER_URL = f"https://api.github.com/users/{GITHUB_USER}"
REST_REPOS_URL = f"https://api.github.com/users/{GITHUB_USER}/repos?per_page=100&sort=pushed"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Profile-Updater)",
    "Accept": "application/vnd.github.v3+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def fetch_graphql_data() -> Dict[str, Any]:
    if not GITHUB_TOKEN:
        return {}

    query = """
    query($user: String!) {
      user(login: $user) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
        repositories(first: 100, ownerAffiliations: OWNER, privacy: PUBLIC) {
          totalCount
          nodes {
            name
            description
            pushedAt
            stargazerCount
            forkCount
            url
            primaryLanguage {
              name
              color
            }
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node {
                  name
                  color
                }
              }
            }
          }
        }
      }
    }
    """
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=json.dumps({"query": query, "variables": {"user": GITHUB_USER}}).encode("utf-8"),
        headers={**HEADERS, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("data", {}).get("user", {})
    except Exception as e:
        print(f"GraphQL request error: {e}")
        return {}


def fetch_rest_fallback() -> Tuple[int, List[Dict[str, Any]]]:
    repo_count = 22
    repos = []
    try:
        req = urllib.request.Request(REST_USER_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            user_data = json.loads(resp.read().decode("utf-8"))
            repo_count = user_data.get("public_repos", 22)
    except Exception as e:
        print(f"REST user error: {e}")

    try:
        req = urllib.request.Request(REST_REPOS_URL, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            repos = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"REST repos error: {e}")

    return repo_count, repos


def compute_metrics() -> Dict[str, Any]:
    graphql = fetch_graphql_data()
    
    if graphql:
        contributions = graphql.get("contributionsCollection", {}).get("contributionCalendar", {}).get("totalContributions", 380)
        repo_nodes = graphql.get("repositories", {}).get("nodes", [])
        total_repos = graphql.get("repositories", {}).get("totalCount", len(repo_nodes))
        
        # Calculate language byte sizes
        lang_sizes: Dict[str, int] = {}
        all_repos = []
        for r in repo_nodes:
            all_repos.append(r)
            edges = r.get("languages", {}).get("edges", [])
            for e in edges:
                name = e["node"]["name"]
                size = e["size"]
                lang_sizes[name] = lang_sizes.get(name, 0) + size
                
        active_repo = None
        for r in all_repos:
            if r["name"] != GITHUB_USER:
                active_repo = r
                break
    else:
        total_repos, repos = fetch_rest_fallback()
        contributions = 380
        lang_sizes = {"Python": 50, "JavaScript": 30, "TypeScript": 12, "Other": 8}
        all_repos = repos
        active_repo = None
        for r in repos:
            if r["name"] != GITHUB_USER:
                active_repo = r
                break

    total_bytes = sum(lang_sizes.values()) or 1
    sorted_langs = sorted(lang_sizes.items(), key=lambda x: x[1], reverse=True)
    
    top_langs = []
    if sorted_langs:
        for name, size in sorted_langs[:4]:
            pct = round((size / total_bytes) * 100)
            top_langs.append((name, pct))
    else:
        top_langs = [("Python", 50), ("JavaScript", 30), ("TypeScript", 12), ("Other", 8)]

    # Format 5 recent repos (excluding the profile repo itself)
    recent_repos = []
    for r in all_repos:
        name = r.get("name", "")
        if name == GITHUB_USER:
            continue
        pushed = r.get("pushedAt") or r.get("pushed_at") or ""
        pushed_date = pushed[:10] if pushed else "Recent"
        desc = r.get("description") or "No description provided."
        if len(desc) > 85:
            desc = desc[:82] + "..."
        
        lang = ""
        if isinstance(r.get("primaryLanguage"), dict):
            lang = r["primaryLanguage"].get("name", "")
        elif r.get("language"):
            lang = r["language"]
        if not lang:
            lang = "Code"

        recent_repos.append({
            "name": name,
            "url": f"https://github.com/{GITHUB_USER}/{name}",
            "desc": desc,
            "lang": lang,
            "updated": pushed_date,
        })
        if len(recent_repos) >= 5:
            break

    return {
        "repos": total_repos,
        "contributions": contributions,
        "top_langs": top_langs,
        "active_repo_name": active_repo["name"] if active_repo else "Google-Forms-Universal-AI-Assistant",
        "active_repo_desc": active_repo.get("description", "AI browser overlay & real-time automation") if active_repo else "AI browser overlay & real-time automation",
        "recent_repos": recent_repos,
    }


def update_stats_bento(metrics: Dict[str, Any], file_path: str) -> bool:
    if not os.path.exists(file_path):
        return False
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content

    # 1. Update public repositories number
    repos_str = f"{metrics['repos']}" if metrics['repos'] >= 20 else f"{metrics['repos']}+"
    content = re.sub(
        r'(<text x="0" y="24" class="bento-num">)[^<]+(</text>\s*<text x="0" y="44" class="bento-sub">Public Repositories</text>)',
        rf'\g<1>{repos_str}\g<2>',
        content,
    )

    # 2. Update contributions number
    contrib_str = f"{metrics['contributions']}+"
    content = re.sub(
        r'(<text x="0" y="24" class="bento-num">)[^<]+(</text>\s*<text x="0" y="44" class="bento-sub">Git Contributions</text>)',
        rf'\g<1>{contrib_str}\g<2>',
        content,
    )

    # 3. Update top languages
    top_langs = metrics["top_langs"]
    if len(top_langs) >= 3:
        l1_name, l1_pct = top_langs[0]
        l1_w = int(280 * (l1_pct / 100))
        content = re.sub(
            r'(<g transform="translate\(20, 50\)">\s*<text [^>]+>)[^<]+(</text>\s*<text [^>]+>)[^<]+(</text>\s*<rect [^>]+/>\s*<rect [^>]+ width=")[^"]+(")',
            rf'\g<1>{l1_name}\g<2>{l1_pct}%\g<3>{l1_w}\g<4>',
            content,
        )

        l2_name, l2_pct = top_langs[1]
        l2_w = int(280 * (l2_pct / 100))
        content = re.sub(
            r'(<g transform="translate\(20, 98\)">\s*<text [^>]+>)[^<]+(</text>\s*<text [^>]+>)[^<]+(</text>\s*<rect [^>]+/>\s*<rect [^>]+ width=")[^"]+(")',
            rf'\g<1>{l2_name}\g<2>{l2_pct}%\g<3>{l2_w}\g<4>',
            content,
        )

        l3_name, l3_pct = top_langs[2]
        l3_w = int(280 * (l3_pct / 100))
        content = re.sub(
            r'(<g transform="translate\(20, 146\)">\s*<text [^>]+>)[^<]+(</text>\s*<text [^>]+>)[^<]+(</text>\s*<rect [^>]+/>\s*<rect [^>]+ width=")[^"]+(")',
            rf'\g<1>{l3_name}\g<2>{l3_pct}%\g<3>{l3_w}\g<4>',
            content,
        )

    # 4. Update Active Horizon
    active_name = metrics["active_repo_name"]
    display_name = active_name if len(active_name) <= 18 else active_name[:17] + "…"
    content = re.sub(
        r'(<text x="12" y="25" fill="#f8edeb"[^>]*>)[^<]+(</text>)',
        rf'\g<1>{display_name}\g<2>',
        content,
    )

    if content != orig_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file_path}")
        return True
    return False


def update_terminal_card(metrics: Dict[str, Any], file_path: str) -> bool:
    if not os.path.exists(file_path):
        return False

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content
    active_name = metrics["active_repo_name"]
    shipping_str = f'"{active_name} 🚀"'

    content = re.sub(
        r'(<tspan class="t-val">shippingNow:</tspan>\s*<tspan class="t-str">)[^<]+(</tspan>)',
        rf'\g<1>{shipping_str}\g<2>',
        content,
    )

    if content != orig_content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {file_path}")
        return True
    return False


def update_readme(metrics: Dict[str, Any], readme_path: str) -> bool:
    if not os.path.exists(readme_path):
        return False

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    orig_content = content
    recent = metrics.get("recent_repos", [])
    if not recent:
        return False

    # Generate recent activity table
    rows = []
    for r in recent:
        row = f"""  <tr>
    <td><b><a href="{r['url']}" style="color: #ffb5a7;">{r['name']}</a></b></td>
    <td style="color: #fcd5ce;">{r['desc']}</td>
    <td align="center"><img src="https://img.shields.io/badge/-{r['lang']}-3a2a37?style=flat-square&labelColor=2b2129&color=ffb5a7" /></td>
    <td align="center"><samp style="color: #f8edeb;">{r['updated']}</samp></td>
  </tr>"""
        rows.append(row)

    table_body = "\n".join(rows)
    new_section = f"""<!-- AUTO_REPOS:START -->
<table align="center" width="100%">
  <thead>
    <tr style="border-bottom: 2px solid #5e4352;">
      <th align="left" style="color: #ffb5a7;">⚡ Repository</th>
      <th align="left" style="color: #ffb5a7;">Overview</th>
      <th align="center" style="color: #ffb5a7;">Stack</th>
      <th align="center" style="color: #ffb5a7;">Pushed</th>
    </tr>
  </thead>
  <tbody>
{table_body}
  </tbody>
</table>
<!-- AUTO_REPOS:END -->"""

    if "<!-- AUTO_REPOS:START -->" in content and "<!-- AUTO_REPOS:END -->" in content:
        content = re.sub(
            r'<!-- AUTO_REPOS:START -->.*?<!-- AUTO_REPOS:END -->',
            new_section,
            content,
            flags=re.DOTALL,
        )
    else:
        # Insert before the Activity Garden section
        insert_marker = '<!-- ═══════════════════ ACTIVITY GARDEN ═══════════════════ -->'
        if insert_marker in content:
            dispatch_block = f"""<!-- ═══════════════════ LIVE DISPATCH: RECENT REPOSITORIES ═══════════════════ -->
<h2 align="center">⚡ Live Repository Dispatch</h2>
<p align="center"><sub>Auto-updated every 6 hours and whenever new repositories or commits are pushed.</sub></p>

{new_section}

<p align="center"><img src="https://raw.githubusercontent.com/REP-Julian/REP-Julian/main/assets/divider.svg" width="650" /></p>

"""
            content = content.replace(insert_marker, dispatch_block + insert_marker)

    if content != orig_content:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {readme_path}")
        return True
    return False


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Syncing profile telemetry for @{GITHUB_USER}...")
    metrics = compute_metrics()
    print("Metrics snapshot:", json.dumps({k: v for k, v in metrics.items() if k != "recent_repos"}, indent=2))
    
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    bento_path = os.path.join(base_dir, "assets", "stats-bento.svg")
    terminal_path = os.path.join(base_dir, "assets", "terminal-card.svg")
    readme_path = os.path.join(base_dir, "README.md")
    
    c1 = update_stats_bento(metrics, bento_path)
    c2 = update_terminal_card(metrics, terminal_path)
    c3 = update_readme(metrics, readme_path)
    
    changed = c1 or c2 or c3
    print(f"Sync complete. Files modified: {changed}")


if __name__ == "__main__":
    main()
