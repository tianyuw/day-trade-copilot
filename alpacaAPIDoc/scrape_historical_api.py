from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

import httpx


ROOT_DIR = Path(__file__).resolve().parent
OUT_ROOT = ROOT_DIR / "historical_api_reference"
REFERENCE_DIR = OUT_ROOT / "reference"
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


def _md_escape(text: str) -> str:
    return text.replace("|", "\\|").strip()


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
    parts.append("# Alpaca Historical API Reference（OpenAPI 索引）")
    parts.append("")
    parts.append(
        "此文件由 `alpacaAPIDoc/historical_api_reference/historical_openapi.yaml` 自动提取生成，便于快速查找每个 REST 端点。"
    )
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


def _extract_operation_from_reference_snapshot(slug: str, md: str) -> OpenAPIOperation | None:
    fence = "```"
    start_idx = md.find("```json")
    if start_idx < 0:
        return None
    content_start = md.find("\n", start_idx)
    if content_start < 0:
        return None
    end_idx = md.find(fence, content_start + 1)
    if end_idx < 0:
        return None
    json_text = md[content_start + 1 : end_idx].strip()
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError:
        return None

    paths = data.get("paths") if isinstance(data, dict) else None
    if not isinstance(paths, dict) or not paths:
        return None
    path = next(iter(paths.keys()))
    methods = paths.get(path)
    if not isinstance(methods, dict) or not methods:
        return None
    method = next(iter(methods.keys()))
    op = methods.get(method)
    if not isinstance(op, dict):
        return None

    tags = op.get("tags")
    tag = tags[0] if isinstance(tags, list) and tags and isinstance(tags[0], str) else None
    summary = op.get("summary") if isinstance(op.get("summary"), str) else None

    return OpenAPIOperation(
        path=str(path),
        method=str(method).upper(),
        operation_id=slug,
        summary=summary,
        tag=tag,
    )


def _render_snapshot_reference_index(reference_dir: Path) -> str:
    ops: list[OpenAPIOperation] = []
    slug_to_source: dict[str, str] = {}
    for p in sorted(reference_dir.glob("*.md")):
        slug = p.stem
        md = p.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^source_view:\s*(\S+)\s*$", md, flags=re.MULTILINE)
        if m:
            slug_to_source[slug] = m.group(1).strip()
        op = _extract_operation_from_reference_snapshot(slug, md)
        if op:
            ops.append(op)

    grouped = _group_by_tag(ops)

    parts: list[str] = []
    parts.append("# Alpaca Historical API Reference（索引）")
    parts.append("")
    parts.append(
        "此文件由 `alpacaAPIDoc/historical_api_reference/reference/*.md` 的 OpenAPI JSON 自动提取生成，优先反映当前 docs.alpaca.markets 的 Reference 结构。"
    )
    parts.append("")

    for tag, tag_ops in grouped.items():
        parts.append(f"## {tag}")
        parts.append("")
        parts.append("| Method | Path | Summary | Snapshot | Source |")
        parts.append("|---|---|---|---|---|")
        for op in tag_ops:
            summary = _md_escape(op.summary or "")
            slug = op.operation_id or ""
            local = reference_dir / f"{_sanitize_basename(slug)}.md"
            rel = local.relative_to(ROOT_DIR).as_posix() if local.exists() else ""
            snapshot_cell = f"[{slug}]({rel})" if rel else ""
            src = slug_to_source.get(slug, _reference_link(slug) or "")
            src_cell = f"[{slug}]({src})" if src else ""
            parts.append(
                f"| {op.method} | {_md_escape(op.path)} | {summary} | {snapshot_cell} | {src_cell} |"
            )
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def _render_snapshot_index(
    items: list[tuple[str, str, Path]], missing: list[tuple[str, str, str]]
) -> str:
    parts: list[str] = []
    parts.append("# Alpaca Historical API Reference（快照目录）")
    parts.append("")
    parts.append("此文件列出本目录下抓取的 `docs.alpaca.markets/reference/*` 页面快照。")
    parts.append("")
    parts.append("| operationId/slug | Source | Local |")
    parts.append("|---|---|---|")
    for key, url, local_path in items:
        rel = local_path.relative_to(ROOT_DIR)
        parts.append(f"| {key} | [{key}]({url}) | {rel.as_posix()} |")
    parts.append("")

    if missing:
        parts.append("## 未抓取成功")
        parts.append("")
        parts.append("| operationId/slug | Source | Reason |")
        parts.append("|---|---|---|")
        for key, url, reason in missing:
            parts.append(f"| {key} | [{key}]({url}) | {_md_escape(reason)} |")
        parts.append("")
    return "\n".join(parts)


def _looks_like_historical_reference(md: str) -> bool:
    if re.search(r"\"title\"\s*:\s*\"Trading API\"", md):
        return False
    if re.search(r"\"title\"\s*:\s*\"Broker API\"", md):
        return False
    if re.search(r"data\.alpaca\.markets", md, flags=re.IGNORECASE):
        return True
    if re.search(r"\bMarket Data\b", md, flags=re.IGNORECASE):
        return True
    if re.search(r"\bHistorical\b", md, flags=re.IGNORECASE):
        return True
    if re.search(r"/v\d+(beta\d+)?/(stocks|crypto|options|news)\b", md, flags=re.IGNORECASE):
        return True
    return False


def _write_reference_snapshots(openapi_yaml: str, scraped_at_utc: str) -> None:
    href_re = re.compile(r'href="(/reference/[^"?#]+)"')

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)

    op_ids = [
        op.operation_id
        for op in _extract_operations_from_openapi_yaml(openapi_yaml)
        if op.operation_id
    ]
    op_id_set = {o for o in op_ids if o}

    written: list[tuple[str, str, Path]] = []
    missing: list[tuple[str, str, str]] = []
    keep: set[Path] = set()

    def write_one(key: str, view_url: str, md_url: str, md: str) -> None:
        header = [
            "---",
            f"source_view: {view_url}",
            f"source_md: {md_url}",
            f"scraped_at_utc: {scraped_at_utc}",
            "---",
            "",
        ]
        local_path = REFERENCE_DIR / f"{_sanitize_basename(key)}.md"
        local_path.write_text("\n".join(header) + md.strip() + "\n", encoding="utf-8")
        written.append((key, view_url, local_path))
        keep.add(local_path)

    with _new_http_client(timeout_s=60.0) as client:
        for op_id in sorted(op_id_set):
            view_url = f"https://docs.alpaca.markets/reference/{op_id}"
            md_url = f"{view_url}.md"
            try:
                md = _fetch_text(md_url, client=client)
            except httpx.HTTPStatusError as e:
                if e.response is not None and e.response.status_code == 404:
                    missing.append((op_id, view_url, "HTTP 404"))
                    continue
                missing.append((op_id, view_url, f"HTTP {e.response.status_code if e.response else 'error'}"))
                continue
            write_one(op_id, view_url, md_url, md)

        landing_html = _fetch_text("https://docs.alpaca.markets/reference", client=client)
        hrefs = sorted(set(href_re.findall(landing_html)))
        slugs = [h.split("/reference/")[-1] for h in hrefs if h.startswith("/reference/")]
        for slug in sorted(set(slugs)):
            if slug in op_id_set:
                continue
            view_url = f"https://docs.alpaca.markets/reference/{slug}"
            md_url = f"{view_url}.md"
            try:
                md = _fetch_text(md_url, client=client)
            except httpx.HTTPStatusError as e:
                if e.response is not None and e.response.status_code == 404:
                    continue
                missing.append((slug, view_url, f"HTTP {e.response.status_code if e.response else 'error'}"))
                continue

            if not _looks_like_historical_reference(md):
                continue
            write_one(slug, view_url, md_url, md)

    for existing in REFERENCE_DIR.glob("*.md"):
        if existing not in keep:
            existing.unlink(missing_ok=True)

    (OUT_ROOT / "historical_api_reference_pages.md").write_text(
        _render_snapshot_index(written, missing),
        encoding="utf-8",
    )


def _write_docs_pages(overview_url: str, scraped_at_utc: str) -> None:
    href_re = re.compile(r'href="(/docs/[^"?#]+)"')

    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    allow_exact = {
        "/docs/about-market-data-api",
        "/docs/getting-started-with-alpaca-market-data",
    }

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
        (OUT_ROOT / "historical_api_overview.md").write_text(
            "\n".join(header) + overview_text + "\n", encoding="utf-8"
        )

        hrefs = sorted(set(href_re.findall(overview_html)))
        paths = []
        for p in hrefs:
            if p.startswith("/docs/historical-") or p in allow_exact:
                paths.append(p)
        paths = sorted(set(paths))

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
    parts.append("# Alpaca Historical API Docs（快照目录）")
    parts.append("")
    parts.append("此文件列出本目录下抓取的 `docs.alpaca.markets/docs/*` 页面快照。")
    parts.append("")
    parts.append("| Page | Source | Local |")
    parts.append("|---|---|---|")
    for slug, url, local_path in rows:
        rel = local_path.relative_to(ROOT_DIR)
        parts.append(f"| {slug} | [{slug}]({url}) | {rel.as_posix()} |")
    parts.append("")
    (OUT_ROOT / "historical_api_docs_pages.md").write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    openapi_url = "https://raw.githubusercontent.com/alpacahq/alpaca-docs/master/oas/data/openapi.yaml"
    historical_overview_url = "https://docs.alpaca.markets/docs/historical-api"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    openapi_yaml = _fetch_text(openapi_url)
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    (OUT_ROOT / "historical_openapi.yaml").write_text(openapi_yaml, encoding="utf-8")
    (OUT_ROOT / "historical_openapi_reference_index.md").write_text(
        _render_openapi_reference_index(openapi_yaml), encoding="utf-8"
    )
    _write_docs_pages(historical_overview_url, scraped_at_utc=now)
    _write_reference_snapshots(openapi_yaml, scraped_at_utc=now)
    (OUT_ROOT / "historical_api_reference_index.md").write_text(
        _render_snapshot_reference_index(REFERENCE_DIR), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
