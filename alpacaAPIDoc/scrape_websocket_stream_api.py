from __future__ import annotations

import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import httpx


ROOT_DIR = Path(__file__).resolve().parent
OUT_ROOT = ROOT_DIR / "websocket_stream_api_reference"
DOCS_DIR = OUT_ROOT / "docs"


class _HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._chunks: list[str] = []
        self._ignore_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript"}:
            self._ignore_depth += 1
            return
        if self._ignore_depth:
            return
        if tag in {"p", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "code"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._ignore_depth:
            self._ignore_depth -= 1
            return
        if self._ignore_depth:
            return
        if tag in {"p", "li"}:
            self._chunks.append("\n")

    def handle_data(self, data: str) -> None:
        if self._ignore_depth:
            return
        if not data.strip():
            return
        self._chunks.append(data)

    def text(self) -> str:
        raw = "".join(self._chunks)
        raw = re.sub(r"[ \t]+\n", "\n", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        raw = re.sub(r"[ \t]{2,}", " ", raw)
        return raw.strip()


def _new_http_client(timeout_s: float = 30.0) -> httpx.Client:
    return httpx.Client(
        timeout=timeout_s,
        follow_redirects=True,
        headers={
            "User-Agent": "day-trade-copilot-docs-scraper/1.0",
            "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        },
    )


def _fetch_text(url: str, timeout_s: float = 30.0, client: httpx.Client | None = None) -> str:
    if client is None:
        with _new_http_client(timeout_s=timeout_s) as c:
            resp = c.get(url)
            resp.raise_for_status()
            return resp.text
    resp = client.get(url)
    resp.raise_for_status()
    return resp.text


def _extract_primary_html_region(html: str) -> str:
    for tag in ("main", "article"):
        m = re.search(
            rf"<{tag}[^>]*>([\s\S]*?)</{tag}>",
            html,
            flags=re.IGNORECASE,
        )
        if m:
            return m.group(1)
    return html


def _html_to_markdown_like_text(html: str) -> str:
    html = _extract_primary_html_region(html)
    parser = _HTMLTextExtractor()
    parser.feed(html)
    return parser.text()


def _sanitize_basename(name: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_.-]+", "_", name.strip())
    safe = safe.strip("._-")
    return safe or "untitled"


def _collect_docs_paths(overview_html: str) -> list[str]:
    href_re = re.compile(r'href="(/docs/[^"?#]+)"')
    hrefs = sorted(set(href_re.findall(overview_html)))

    deny_exact = {
        "/docs/websocket-streaming",
    }

    allow_exact = {
        "/docs/streaming-market-data",
        "/docs/real-time-stock-pricing-data",
        "/docs/real-time-crypto-pricing-data",
        "/docs/real-time-option-data",
        "/docs/streaming-real-time-news",
    }

    paths: set[str] = set()
    for p in hrefs:
        if p in deny_exact:
            continue
        if p in allow_exact:
            paths.add(p)
            continue
        lower = p.lower()
        if "stream" in lower or "websocket" in lower:
            paths.add(p)
            continue
        if lower.startswith("/docs/real-time-") and ("data" in lower or "news" in lower):
            paths.add(p)

    paths.update(allow_exact)
    return sorted(paths)


def _write_pages(overview_url: str, scraped_at_utc: str) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    with _new_http_client(timeout_s=60.0) as client:
        overview_html = _fetch_text(overview_url, client=client)
        overview_text = _html_to_markdown_like_text(overview_html)
        header = [
            "---",
            f"source: {overview_url}",
            f"scraped_at_utc: {scraped_at_utc}",
            "---",
            "",
        ]
        (OUT_ROOT / "websocket_stream_overview.md").write_text(
            "\n".join(header) + overview_text + "\n", encoding="utf-8"
        )

        paths = _collect_docs_paths(overview_html)
        keep: set[Path] = set()
        rows: list[tuple[str, str, Path]] = []

        for path in paths:
            slug = _sanitize_basename(path.split("/docs/")[-1])
            url = f"https://docs.alpaca.markets{path}"
            html = _fetch_text(url, client=client)
            text = _html_to_markdown_like_text(html)
            header = [
                "---",
                f"source: {url}",
                f"scraped_at_utc: {scraped_at_utc}",
                "---",
                "",
            ]
            local_path = DOCS_DIR / f"{slug}.md"
            local_path.write_text("\n".join(header) + text + "\n", encoding="utf-8")
            keep.add(local_path)
            rows.append((slug, url, local_path))

        for existing in DOCS_DIR.glob("*.md"):
            if existing not in keep:
                existing.unlink(missing_ok=True)

    parts: list[str] = []
    parts.append("# Alpaca WebSocket Stream Docs（快照目录）")
    parts.append("")
    parts.append("此文件列出本目录下抓取的 WebSocket Stream 相关页面快照（docs.alpaca.markets/docs/*）。")
    parts.append("")
    parts.append("| Page | Source | Local |")
    parts.append("|---|---|---|")
    for slug, url, local_path in rows:
        rel = local_path.relative_to(ROOT_DIR)
        parts.append(f"| {slug} | [{slug}]({url}) | {rel.as_posix()} |")
    parts.append("")
    (OUT_ROOT / "websocket_stream_docs_pages.md").write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    overview_url = "https://docs.alpaca.markets/docs/streaming-market-data"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    _write_pages(overview_url, scraped_at_utc=now)


if __name__ == "__main__":
    main()
