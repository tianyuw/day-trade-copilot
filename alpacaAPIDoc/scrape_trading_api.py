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


def _render_reference_index(openapi_yaml: str) -> str:
    ops = _extract_operations_from_openapi_yaml(openapi_yaml)
    grouped = _group_by_tag(ops)

    parts: list[str] = []
    parts.append("# Alpaca Trading API Reference（索引）")
    parts.append("")
    parts.append(
        "此文件由 `alpacaAPIDoc/trading_openapi.yaml` 自动提取生成，便于快速查找每个 REST 端点。"
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


def _render_reference_snapshot_index(
    items: list[tuple[str, str, Path]], missing: list[tuple[str, str, str]]
) -> str:
    parts: list[str] = []
    parts.append("# Alpaca Trading API Reference（快照目录）")
    parts.append("")
    parts.append("此文件列出本目录下抓取的 `docs.alpaca.markets/reference/*` 页面快照。")
    parts.append("")
    parts.append("| operationId | Source | Local |")
    parts.append("|---|---|---|")
    for operation_id, url, local_path in items:
        rel = local_path.relative_to(ROOT_DIR)
        parts.append(f"| {operation_id} | [{operation_id}]({url}) | {rel.as_posix()} |")
    parts.append("")

    if missing:
        parts.append("## 未抓取成功")
        parts.append("")
        parts.append("| operationId | Source | Reason |")
        parts.append("|---|---|---|")
        for operation_id, url, reason in missing:
            parts.append(f"| {operation_id} | [{operation_id}]({url}) | {_md_escape(reason)} |")
        parts.append("")
    return "\n".join(parts)


def _write_reference_snapshots(openapi_yaml: str, scraped_at_utc: str) -> None:
    trading_title_re = re.compile(r"\"title\"\s*:\s*\"Trading API\"")
    href_re = re.compile(r"href=\"(/reference/[^\"?#]+)\"")

    out_dir = ROOT_DIR / "trading_reference"
    out_dir.mkdir(parents=True, exist_ok=True)

    with _new_http_client(timeout_s=60.0) as client:
        landing_html = _fetch_text("https://docs.alpaca.markets/reference", client=client)
        hrefs = sorted(set(href_re.findall(landing_html)))
        slugs = [h.split("/reference/")[-1] for h in hrefs if h.startswith("/reference/")]

        written: list[tuple[str, str, Path]] = []
        missing: list[tuple[str, str, str]] = []
        keep: set[Path] = set()

        for slug in sorted(set(slugs)):
            view_url = f"https://docs.alpaca.markets/reference/{slug}"
            md_url = f"{view_url}.md"
            try:
                md = _fetch_text(md_url, client=client)
            except httpx.HTTPStatusError as e:
                if e.response is not None and e.response.status_code == 404:
                    continue
                missing.append((slug, view_url, f"HTTP {e.response.status_code if e.response else 'error'}"))
                continue

            if not trading_title_re.search(md):
                continue

            header = [
                "---",
                f"source_view: {view_url}",
                f"source_md: {md_url}",
                f"scraped_at_utc: {scraped_at_utc}",
                "---",
                "",
            ]
            local_path = out_dir / f"{slug}.md"
            local_path.write_text("\n".join(header) + md.strip() + "\n", encoding="utf-8")
            written.append((slug, view_url, local_path))
            keep.add(local_path)

        for existing in out_dir.glob("*.md"):
            if existing not in keep:
                existing.unlink(missing_ok=True)

    (ROOT_DIR / "trading_api_reference_pages.md").write_text(
        _render_reference_snapshot_index(written, missing),
        encoding="utf-8",
    )


def main() -> None:
    trading_openapi_url = "https://raw.githubusercontent.com/alpacahq/alpaca-docs/master/oas/trading/openapi.yaml"
    trading_overview_url = "https://docs.alpaca.markets/docs/trading-api"

    openapi_yaml = _fetch_text(trading_openapi_url)
    overview_html = _fetch_text(trading_overview_url)
    overview_text = _html_to_markdown_like_text(overview_html)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    header = [
        "---",
        f"source: {trading_overview_url}",
        f"scraped_at_utc: {now}",
        "---",
        "",
    ]

    (ROOT_DIR / "trading_openapi.yaml").write_text(openapi_yaml, encoding="utf-8")
    (ROOT_DIR / "trading_api_overview.md").write_text(
        "\n".join(header) + overview_text + "\n", encoding="utf-8"
    )
    (ROOT_DIR / "trading_api_reference_index.md").write_text(
        _render_reference_index(openapi_yaml), encoding="utf-8"
    )
    _write_reference_snapshots(openapi_yaml, scraped_at_utc=now)


if __name__ == "__main__":
    main()
