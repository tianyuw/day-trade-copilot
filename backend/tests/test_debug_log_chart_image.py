import os
import base64
from pathlib import Path

from app.debug_logging import LLMExchangeMeta, write_llm_exchange


PNG_1X1_BASE64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8"
    "/w8AAusB9Yg0g0wAAAAASUVORK5CYII="
)


def _assert_written(json_path: Path, expected_png_bytes: bytes) -> None:
    assert json_path.exists(), f"missing json: {json_path}"
    png_path = json_path.with_suffix(".png")
    assert png_path.exists(), f"missing png: {png_path}"
    assert png_path.read_bytes() == expected_png_bytes, "png bytes mismatch"


def test_debug_log_writes_chart_png(tmp_path, monkeypatch) -> None:
    expected_png_bytes = base64.b64decode(PNG_1X1_BASE64)
    monkeypatch.setenv("OUTPUT_DEBUG_LOG", "true")
    monkeypatch.setenv("DEBUG_LOG_DIR", str(tmp_path))

    json_path_1 = write_llm_exchange(
        meta=LLMExchangeMeta(kind="analysis", symbol="TEST", analysis_id="a1"),
        system_prompt="s",
        user_prompt="u",
        chart_image_base64=PNG_1X1_BASE64,
        response_raw="{}",
        parsed_json={},
        error=None,
        duration_ms=1,
    )
    assert json_path_1 is not None
    _assert_written(json_path_1, expected_png_bytes)

    json_path_2 = write_llm_exchange(
        meta=LLMExchangeMeta(kind="position_management", symbol="TEST", trade_id="t1"),
        system_prompt="s",
        user_prompt="u",
        chart_image_base64=f"data:image/png;base64,{PNG_1X1_BASE64}",
        response_raw="{}",
        parsed_json={},
        error=None,
        duration_ms=1,
    )
    assert json_path_2 is not None
    _assert_written(json_path_2, expected_png_bytes)
