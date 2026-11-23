#!/usr/bin/env python3
"""Refresh public Pages links and previews when their source commits change."""

import base64
import html
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlparse
from urllib.request import Request, urlopen

OWNER = "lprakashv"
ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- apps:start -->", "<!-- apps:end -->"
PROFILE_START, PROFILE_END = "<!-- pages:start -->", "<!-- pages:end -->"
PROFILE_CARDS = {"dsa-blueprint", "designed-to-scale", "codenames-game", "cleanwall-plus-ultra"}
DOMAIN = re.compile(r"https?://(?:www\.)?lprakashv\.com/[^\s<>)\]\"']+", re.I)
PAGES = re.compile(r"https?://lprakashv\.github\.io/[^\s<>)\]\"']+", re.I)
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^\s)]+)(?:\s+[^)]*)?\)|<img\b[^>]*?src=["\']([^"\']+)["\'][^>]*>', re.I)


def request(url):
    headers = {"User-Agent": "profile-app-index", "Accept": "application/vnd.github+json"}
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]
    return urlopen(Request(url, headers=headers), timeout=30)


def api(path):
    with request("https://api.github.com" + path) as response:
        return json.load(response)


def readme(repo, sha):
    try:
        data = api(f"/repos/{OWNER}/{repo['name']}/readme?ref={quote(sha)}")
    except HTTPError as error:
        if error.code == 404:
            return ""
        raise
    return base64.b64decode(data["content"]).decode("utf-8")


def app_url(repo, content):
    urls = [repo.get("homepage") or "", *DOMAIN.findall(content), *PAGES.findall(content)]
    # A Pages project can be discoverable even without a homepage or README link.
    urls.append(f"https://{OWNER}.github.io/{repo['name']}/")
    for value in urls:
        parsed = urlparse(value)
        if parsed.hostname == f"{OWNER}.github.io" and parsed.path.strip("/").lower() == repo["name"].lower():
            try:
                with request(value) as response:
                    parsed = urlparse(response.geturl())
            except HTTPError as error:
                if error.code == 404:
                    continue
                raise
        if parsed.scheme in ("https", "http") and parsed.hostname in ("lprakashv.com", "www.lprakashv.com") and parsed.path.strip("/"):
            return "https://www.lprakashv.com" + parsed.path.rstrip("/") + "/"
    return None


def image_url(repo, content, sha):
    matches = list(IMAGE.finditer(content))
    matches.sort(key=lambda match: not bool(re.search(r"screenshot|showcase|demo|docs/images", match[0], re.I)))
    for match in matches:
        alt, target, html_target = match.groups()
        target = html.unescape(target or html_target)
        if re.search(r"badge|shield|logo|icon", (alt or "") + " " + target, re.I):
            continue
        if not re.search(r"\.(?:png|jpe?g|gif|webp)(?:\?.*)?$", target, re.I):
            continue
        if target.startswith("https://"):
            url = target
        elif not target.startswith(("/", "http:", "//", "data:")):
            base = f"https://raw.githubusercontent.com/{OWNER}/{repo['name']}/{sha}/"
            url = urljoin(base, quote(target, safe="/.-_~"))
        else:
            continue
        try:
            with request(url) as response:
                if response.headers.get_content_type().startswith("image/"):
                    return url
        except HTTPError as error:
            if error.code == 404:
                continue
            raise
    return None


def entries(profile=False):
    repos, page = [], 1
    while True:
        batch = api(f"/users/{OWNER}/repos?type=owner&per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    cache_path = ROOT / ".app-sync-state.json"
    previous = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    updated = {}
    first_run_failures = []
    for repo in sorted(repos, key=lambda item: item["name"].lower()):
        name = repo["name"]
        if repo["private"] or repo["fork"] or (not repo["has_pages"] and not (profile and name in PROFILE_CARDS)) or name == f"{OWNER}.github.io":
            continue
        old = previous.get(name)
        try:
            sha = api(f"/repos/{OWNER}/{name}/commits/{quote(repo['default_branch'], safe='')}")["sha"]
            if old and old["sha"] == sha:
                updated[name] = old
                continue
            content = readme(repo, sha)
            url = app_url(repo, content) if repo["has_pages"] else None
            preview = image_url(repo, content, sha) if url or name in PROFILE_CARDS and profile else None
            if (url or name in PROFILE_CARDS and profile) and not preview:
                print(f"{name}: no usable README image; using a text link")
            updated[name] = {"sha": sha, "url": url, "image": preview,
                             "description": repo.get("description") or "", "repo": repo["html_url"]}
        except (HTTPError, URLError, TimeoutError, KeyError, ValueError) as error:
            print(f"{name}: update failed ({error}); retaining the last successful entry", file=sys.stderr)
            if old:
                updated[name] = old
            elif not cache_path.exists():
                first_run_failures.append(name)
    if first_run_failures:
        raise RuntimeError("Initial sync failed for: " + ", ".join(first_run_failures))
    return cache_path, updated


def render(items):
    blocks = []
    for name, item in items.items():
        if not item["url"]:
            continue
        description = html.escape(item["description"], quote=False).replace("\n", " ")
        lines = [f"### [{name}]({item['url']})", "", description, "", f"[Repository]({item['repo']})"]
        if item["image"]:
            lines += ["", f"![{name} app preview]({item['image']})"]
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


def main():
    profile = "--profile" in sys.argv[1:]
    cache_path, items = entries(profile)
    path = ROOT / "README.md"
    text = path.read_text()
    start, end = (PROFILE_START, PROFILE_END) if profile else (START, END)
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) > text.index(end):
        raise ValueError("README app markers are missing or invalid")
    if profile:
        # Keep the hand-written cards and links; update only each card's image.
        for name in PROFILE_CARDS:
            item = items.get(name, {})
            if not item.get("image"):
                continue
            cell = re.compile(r'<td\b[^>]*>[^\n]*?https://github\.com/lprakashv/' + re.escape(name) + r'[^\n]*?</td>')
            text = cell.sub(lambda match: re.sub(r'(<img\s+src=")[^"]+', lambda image: image[1] + html.escape(item["image"], quote=True), match[0], count=1), text, count=1)
        before, rest = text.split(start, 1)
        _, after = rest.split(end, 1)
        existing = before + after
        lines = []
        for name, item in items.items():
            if item["url"] and not re.search(r'https://github\.com/lprakashv/' + re.escape(name) + r'(?=[/\"\)#?]|$)', existing):
                lines.append(f"- 🌐 [{name}]({item['url']}) · [Repository]({item['repo']})")
                if item["image"]:
                    lines.append(f"\n  ![{name} app preview]({item['image']})")
        content = "\n".join(lines)
    else:
        content = render(items)
    if not profile and not content:
        raise RuntimeError("No matching apps found; keeping the existing README and state.")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    body = "\n\n" + content + "\n\n" if content else "\n\n"
    path.write_text(before + start + body + end + after)
    cache_path.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
