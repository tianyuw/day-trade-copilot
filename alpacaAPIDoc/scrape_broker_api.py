from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

import httpx


ROOT_DIR = Path(__file__).resolve().parent


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


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|").strip()


def _safe_basename(raw: str) -> str:
    raw = raw.strip().strip("/")
    if not raw:
        return "index"
    raw = raw.replace("/", "-")
    raw = re.sub(r"[^a-zA-Z0-9._-]+", "-", raw)
    raw = re.sub(r"-{2,}", "-", raw)
    return raw.strip("-") or "index"


@dataclass(frozen=True)
class OpenAPIOperation:
    path: str
    method: str
    operation_id: str | None
    summary: str | None
    tag: str | None


_PATH_LINE_RE = re.compile(r"^  ['\"]?(/[^'\"]+)['\"]?:\s*$")
_METHOD_LINE_RE = re.compile(r"^    (get|post|put|patch|delete|head|options|trace):\s*$")
_OPID_RE = re.compile(r"^      operationId:\s*(.+?)\s*$")
_SUMMARY_RE = re.compile(r"^      summary:\s*(.+?)\s*$")
_TAGS_START_RE = re.compile(r"^      tags:\s*$")
_TAG_ITEM_RE = re.compile(r"^        -\s*(.+?)\s*$")


def _extract_operations_from_openapi_yaml(openapi_yaml: str) -> list[OpenAPIOperation]:
    lines = openapi_yaml.splitlines()
    in_paths = False
    current_path: str | None = None
    current_method: str | None = None
    in_tags = False
    current_tag: str | None = None
    current_op_id: str | None = None
    current_summary: str | None = None

    ops: list[OpenAPIOperation] = []

    def flush() -> None:
        nonlocal current_path, current_method, current_op_id, current_summary, current_tag
        if current_path and current_method:
            ops.append(
                OpenAPIOperation(
                    path=current_path,
                    method=current_method.upper(),
                    operation_id=current_op_id,
                    summary=current_summary,
                    tag=current_tag,
                )
            )
        current_method = None
        current_op_id = None
        current_summary = None
        current_tag = None

    for line in lines:
        if not in_paths:
            if line.strip() == "paths:":
                in_paths = True
            continue

        m_path = _PATH_LINE_RE.match(line)
        if m_path:
            flush()
            current_path = m_path.group(1)
            in_tags = False
            continue

        m_method = _METHOD_LINE_RE.match(line)
        if m_method:
            flush()
            current_method = m_method.group(1)
            in_tags = False
            continue

        if current_method is None:
            continue

        m_opid = _OPID_RE.match(line)
        if m_opid:
            current_op_id = m_opid.group(1).strip().strip("'").strip('"')
            continue

        m_sum = _SUMMARY_RE.match(line)
        if m_sum:
            current_summary = m_sum.group(1).strip().strip("'").strip('"')
            continue

        if _TAGS_START_RE.match(line):
            in_tags = True
            continue

        if in_tags:
            m_tag = _TAG_ITEM_RE.match(line)
            if m_tag:
                current_tag = m_tag.group(1).strip().strip("'").strip('"')
                in_tags = False
            elif line.startswith("      ") and line.strip():
                in_tags = False

        if line and not line.startswith(" "):
            break

    flush()
    unique: dict[tuple[str, str], OpenAPIOperation] = {}
    for op in ops:
        unique[(op.method, op.path)] = op
    return sorted(unique.values(), key=lambda o: (o.tag or "", o.path, o.method))


def _group_by_tag(ops: Iterable[OpenAPIOperation]) -> dict[str, list[OpenAPIOperation]]:
    grouped: dict[str, list[OpenAPIOperation]] = {}
    for op in ops:
        tag = op.tag or "Untagged"
        grouped.setdefault(tag, []).append(op)
    for tag in grouped:
        grouped[tag] = sorted(grouped[tag], key=lambda o: (o.path, o.method))
    return dict(sorted(grouped.items(), key=lambda kv: kv[0].lower()))


def _reference_link(operation_id: str | None) -> str | None:
    if not operation_id:
        return None
    safe = operation_id.strip()
    if not safe:
        return None
    return f"https://docs.alpaca.markets/reference/{safe}"


def _render_openapi_reference_index(openapi_yaml: str) -> str:
    ops = _extract_operations_from_openapi_yaml(openapi_yaml)
    grouped = _group_by_tag(ops)

    parts: list[str] = []
    parts.append("# Alpaca Broker API Reference（OpenAPI 索引）")
    parts.append("")
    parts.append("此文件由 `broker_openapi.yaml` 自动提取生成，便于快速查找每个 REST 端点。")
    parts.append("")

    for tag, tag_ops in grouped.items():
        parts.append(f"## {tag}")
        parts.append("")
        parts.append("| Method | Path | Summary | Reference |")
        parts.append("|---|---|---|---|")
        for op in tag_ops:
            summary = _md_escape(op.summary or "")
            ref = _reference_link(op.operation_id)
            ref_cell = f"[{op.operation_id}]({ref})" if ref else ""
            parts.append(f"| {op.method} | {_md_escape(op.path)} | {summary} | {ref_cell} |")
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def _extract_doc_paths_from_html(html: str) -> set[str]:
    href_re = re.compile(r'href="([^"#?]+)"')
    primary = _extract_primary_html_region(html)
    found: set[str] = set()
    for href in href_re.findall(primary):
        if href.startswith("https://docs.alpaca.markets/docs/"):
            href = href.replace("https://docs.alpaca.markets", "")
        if href.startswith("/docs/"):
            found.add(href.rstrip("/"))
    return found


def _looks_like_broker_docs_html(html: str) -> bool:
    primary = _extract_primary_html_region(html)
    hay = primary.lower()
    if "broker api" in hay:
        return True
    if "broker-api.alpaca.markets" in hay or "broker-api.sandbox.alpaca.markets" in hay:
        return True
    if "/v1/accounts" in hay and "broker" in hay:
        return True
    return False


def _collect_broker_docs_paths(
    overview_html: str, client: httpx.Client, max_pages: int = 80, max_depth: int = 2
) -> list[str]:
    seeds = sorted(_extract_doc_paths_from_html(overview_html) | {"/docs/about-broker-api"})
    queue: list[tuple[str, int]] = [(p, 0) for p in seeds]
    visited: set[str] = set()
    accepted: set[str] = set()

    deny_keywords = (
        "historical",
        "market-data",
        "stream",
        "streaming",
        "websocket",
        "real-time",
        "trading-api",
        "trading-api",
        "options",
        "news",
        "crypto",
    )

    while queue and len(visited) < max_pages:
        path, depth = queue.pop(0)
        if path in visited:
            continue
        visited.add(path)

        if any(k in path for k in deny_keywords):
            continue

        url = f"https://docs.alpaca.markets{path}"
        try:
            html = _fetch_text(url, client=client)
        except httpx.HTTPStatusError:
            continue

        if _looks_like_broker_docs_html(html):
            accepted.add(path)

        if depth >= max_depth:
            continue

        for nxt in sorted(_extract_doc_paths_from_html(html)):
            if nxt in visited:
                continue
            if any(k in nxt for k in deny_keywords):
                continue
            queue.append((nxt, depth + 1))

    return sorted(accepted)


def _render_docs_pages_index(items: list[tuple[str, str, Path]]) -> str:
    parts: list[str] = []
    parts.append("# Alpaca Broker API Docs（快照目录）")
    parts.append("")
    parts.append("此文件列出本目录下抓取的 `docs.alpaca.markets/docs/*` 页面快照。")
    parts.append("")
    parts.append("| Doc | Source | Local |")
    parts.append("|---|---|---|")
    for doc_path, url, local_path in items:
        rel = local_path.relative_to(ROOT_DIR)
        parts.append(f"| {doc_path} | [{doc_path}]({url}) | {rel.as_posix()} |")
    parts.append("")
    return "\n".join(parts)


def _write_docs_pages(overview_html: str, out_dir: Path, scraped_at_utc: str) -> None:
    docs_dir = out_dir / "docs"
    docs_dir.mkdir(parents=True, exist_ok=True)

    with _new_http_client(timeout_s=60.0) as client:
        paths = _collect_broker_docs_paths(overview_html, client=client)
        written: list[tuple[str, str, Path]] = []
        keep: set[Path] = set()

        for p in paths:
            url = f"https://docs.alpaca.markets{p}"
            html = _fetch_text(url, client=client)
            text = _html_to_markdown_like_text(html)

            slug = _safe_basename(p.split("/docs/")[-1])
            local_path = docs_dir / f"{slug}.md"
            header = [
                "---",
                f"source: {url}",
                f"scraped_at_utc: {scraped_at_utc}",
                "---",
                "",
            ]
            local_path.write_text("\n".join(header) + text + "\n", encoding="utf-8")
            written.append((p, url, local_path))
            keep.add(local_path)

        for existing in docs_dir.glob("*.md"):
            if existing not in keep:
                existing.unlink(missing_ok=True)

    (out_dir / "broker_api_docs_pages.md").write_text(
        _render_docs_pages_index(written),
        encoding="utf-8",
    )


def _looks_like_broker_reference_md(md: str) -> bool:
    if re.search(r"\"title\"\s*:\s*\"Broker API\"", md):
        return True
    lower = md.lower()
    if "broker-api.alpaca.markets" in lower or "broker-api.sandbox.alpaca.markets" in lower:
        return True
    if "broker dashboard" in lower and "api reference" in lower:
        return True
    return False


def _render_reference_snapshot_index(
    items: list[tuple[str, str, Path]], missing: list[tuple[str, str, str]]
) -> str:
    parts: list[str] = []
    parts.append("# Alpaca Broker API Reference（快照目录）")
    parts.append("")
    parts.append("此文件列出本目录下抓取的 `docs.alpaca.markets/reference/*` 页面快照。")
    parts.append("")
    parts.append("| operationId/slug | Source | Local |")
    parts.append("|---|---|---|")
    for slug, url, local_path in items:
        rel = local_path.relative_to(ROOT_DIR)
        parts.append(f"| {slug} | [{slug}]({url}) | {rel.as_posix()} |")
    parts.append("")

    if missing:
        parts.append("## 未抓取成功")
        parts.append("")
        parts.append("| operationId/slug | Source | Reason |")
        parts.append("|---|---|---|")
        for slug, url, reason in missing:
            parts.append(f"| {slug} | [{slug}]({url}) | {_md_escape(reason)} |")
        parts.append("")

    return "\n".join(parts)


def _write_reference_snapshots(openapi_yaml: str, out_dir: Path, scraped_at_utc: str) -> None:
    href_re = re.compile(r"href=\"(/reference/[^\"?#]+)\"")
    ops = _extract_operations_from_openapi_yaml(openapi_yaml)
    op_ids = sorted({op.operation_id for op in ops if op.operation_id})
    op_id_set = set(op_ids)

    ref_dir = out_dir / "reference"
    ref_dir.mkdir(parents=True, exist_ok=True)

    with _new_http_client(timeout_s=60.0) as client:
        written: list[tuple[str, str, Path]] = []
        missing: list[tuple[str, str, str]] = []
        keep: set[Path] = set()

        def try_write(slug: str, force: bool = False) -> None:
            view_url = f"https://docs.alpaca.markets/reference/{slug}"
            md_url = f"{view_url}.md"
            try:
                md = _fetch_text(md_url, client=client)
            except httpx.HTTPStatusError as e:
                if e.response is not None and e.response.status_code == 404:
                    missing.append((slug, view_url, "HTTP 404"))
                    return
                missing.append((slug, view_url, f"HTTP {e.response.status_code if e.response else 'error'}"))
                return

            if not force and not _looks_like_broker_reference_md(md):
                return

            header = [
                "---",
                f"source_view: {view_url}",
                f"source_md: {md_url}",
                f"scraped_at_utc: {scraped_at_utc}",
                "---",
                "",
            ]
            local_path = ref_dir / f"{_safe_basename(slug)}.md"
            local_path.write_text("\n".join(header) + md.strip() + "\n", encoding="utf-8")
            written.append((slug, view_url, local_path))
            keep.add(local_path)

        for op_id in op_ids:
            try_write(op_id, force=True)

        landing_html = _fetch_text("https://docs.alpaca.markets/reference", client=client)
        hrefs = sorted(set(href_re.findall(landing_html)))
        slugs = [h.split("/reference/")[-1] for h in hrefs if h.startswith("/reference/")]

        keyword_slugs = [
            s
            for s in slugs
            if any(
                k in s.lower()
                for k in (
                    "account",
                    "accounts",
                    "document",
                    "disclosure",
                    "bank",
                    "ach",
                    "wire",
                    "transfer",
                    "journal",
                    "relationship",
                    "event",
                    "sse",
                    "trading",
                    "positions",
                    "orders",
                    "asset",
                    "cash",
                    "fee",
                    "kyc",
                )
            )
        ]
        keyword_slugs = sorted(set(keyword_slugs))
        for slug in keyword_slugs[:250]:
            if slug in op_id_set:
                continue
            try_write(slug, force=False)

        for existing in ref_dir.glob("*.md"):
            if existing not in keep:
                existing.unlink(missing_ok=True)

    (out_dir / "broker_api_reference_pages.md").write_text(
        _render_reference_snapshot_index(written, missing),
        encoding="utf-8",
    )


def main() -> None:
    broker_overview_url = "https://docs.alpaca.markets/docs/about-broker-api"
    broker_openapi_url = "https://raw.githubusercontent.com/alpacahq/alpaca-docs/master/oas/broker/openapi.yaml"

    out_dir = ROOT_DIR / "broker_api_reference"
    out_dir.mkdir(parents=True, exist_ok=True)

    openapi_yaml = _fetch_text(broker_openapi_url)
    overview_html = _fetch_text(broker_overview_url)
    overview_text = _html_to_markdown_like_text(overview_html)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = [
        "---",
        f"source: {broker_overview_url}",
        f"scraped_at_utc: {now}",
        "---",
        "",
    ]

    (out_dir / "broker_openapi.yaml").write_text(openapi_yaml, encoding="utf-8")
    (out_dir / "broker_api_overview.md").write_text(
        "\n".join(header) + overview_text + "\n", encoding="utf-8"
    )
    (out_dir / "broker_openapi_reference_index.md").write_text(
        _render_openapi_reference_index(openapi_yaml),
        encoding="utf-8",
    )

    _write_docs_pages(overview_html, out_dir=out_dir, scraped_at_utc=now)
    _write_reference_snapshots(openapi_yaml, out_dir=out_dir, scraped_at_utc=now)


if __name__ == "__main__":
    main()
