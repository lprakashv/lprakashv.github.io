#!/usr/bin/env python3
"""Refresh the README app list from public GitHub Pages repositories."""

import base64
import html
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

OWNER = "lprakashv"
ROOT = Path(__file__).resolve().parent.parent
START = "<!-- apps:start -->"
END = "<!-- apps:end -->"
DOMAIN = re.compile(r"https?://(?:www\.)?lprakashv\.com/[^\s<>)\]\"']+", re.I)
PAGES = re.compile(r"https?://lprakashv\.github\.io/[^\s<>)\]\"']+", re.I)
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^\s)]+)(?:\s+[^)]*)?\)|<img\b[^>]*?src=["\']([^"\']+)["\'][^>]*>', re.I)


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "site-app-index"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    with urlopen(Request("https://api.github.com" + path, headers=headers), timeout=30) as response:
        return json.load(response)


def readme(repo):
    try:
        data = api(f"/repos/{OWNER}/{repo['name']}/readme")
    except HTTPError as error:
        if error.code == 404:
            return ""
        raise
    return base64.b64decode(data["content"]).decode("utf-8")


def app_url(repo, content):
    # Pages project URLs can redirect from github.io to the custom domain.
    urls = [repo.get("homepage") or "", *DOMAIN.findall(content), *PAGES.findall(content)]
    for value in urls:
        parsed = urlparse(value)
        if parsed.hostname == f"{OWNER}.github.io" and parsed.path.strip("/").lower() == repo["name"].lower():
            request = Request(value, headers={"User-Agent": "site-app-index"})
            with urlopen(request, timeout=30) as response:
                parsed = urlparse(response.geturl())
        if parsed.scheme in ("https", "http") and parsed.hostname in ("lprakashv.com", "www.lprakashv.com") and parsed.path.strip("/"):
            return "https://www.lprakashv.com" + parsed.path.rstrip("/") + "/"
    return None


def image_url(repo, content):
    for match in IMAGE.finditer(content):
        alt, target, html_target = match.groups()
        target = html.unescape(target or html_target)
        if re.search(r"badge|shield|logo|icon", (alt or "") + " " + target, re.I):
            continue
        if not re.search(r"\.(?:png|jpe?g|gif|webp)(?:\?.*)?$", target, re.I):
            continue
        if target.startswith("https://"):
            return target
        if not target.startswith(("/", "http:", "//", "data:")):
            base = f"https://raw.githubusercontent.com/{OWNER}/{repo['name']}/{quote(repo['default_branch'], safe='')}/"
            return urljoin(base, quote(target, safe="/.-_~"))
    return None


def render(repos):
    entries = []
    for repo in sorted(repos, key=lambda item: item["name"].lower()):
        if repo["private"] or not repo["has_pages"] or repo["name"] == f"{OWNER}.github.io":
            continue
        content = readme(repo)
        url = app_url(repo, content)
        if not url:
            continue
        name = repo["name"]
        description = html.escape(repo.get("description") or "", quote=False).replace("\n", " ")
        screenshot = image_url(repo, content)
        lines = [f"### [{name}]({url})", "", description, "", f"[Repository]({repo['html_url']})"]
        if screenshot:
            lines += ["", f"![{name} app preview]({screenshot})"]
        entries.append("\n".join(lines))
    return "\n\n".join(entries)


def main():
    repos = []
    page = 1
    while True:
        batch = api(f"/users/{OWNER}/repos?type=owner&per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    content = render(repos)
    if not content:
        raise RuntimeError("No matching apps found; keeping the existing README.")
    path = ROOT / "README.md"
    text = path.read_text()
    if text.count(START) != 1 or text.count(END) != 1 or text.index(START) > text.index(END):
        raise ValueError("README app markers are missing or invalid")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    path.write_text(before + START + "\n\n" + content + "\n\n" + END + after)


if __name__ == "__main__":
    main()
