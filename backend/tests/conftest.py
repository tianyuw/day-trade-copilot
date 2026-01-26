import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv


def _fail_fast_missing_env(var_names: list[str]) -> None:
    missing = [k for k in var_names if not (os.getenv(k) or "").strip()]
    if missing:
        raise RuntimeError(f"Missing required env vars for tests: {', '.join(missing)}")


def pytest_sessionstart(session):
    backend_dir = Path(__file__).resolve().parents[1]
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))

    load_dotenv(dotenv_path=backend_dir / ".env")

    _fail_fast_missing_env(
        [
            "GOOGLE_API_KEY",
            "ALPACA_API_KEY",
            "ALPACA_SECRET_KEY",
        ]
    )


def pytest_configure(config):
    config._llm_backtest_results = []


def pytest_sessionfinish(session, exitstatus):
    results = getattr(session.config, "_llm_backtest_results", None)
    if not isinstance(results, list) or not results:
        return

    passed = sum(1 for r in results if isinstance(r, dict) and r.get("passed") is True)
    total = sum(1 for r in results if isinstance(r, dict) and "passed" in r)
    pass_rate = (passed / total) if total else 0.0

    backend_dir = Path(__file__).resolve().parents[1]
    out_dir = backend_dir / "test_reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "llm_backtest_report.json"
    payload = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": pass_rate,
        "results": results,
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    results = getattr(config, "_llm_backtest_results", None)
    if not isinstance(results, list) or not results:
        return

    passed = sum(1 for r in results if isinstance(r, dict) and r.get("passed") is True)
    total = sum(1 for r in results if isinstance(r, dict) and "passed" in r)
    pass_rate = (passed / total) if total else 0.0
    terminalreporter.write_sep("-", f"LLM backtest pass rate: {passed}/{total} ({pass_rate:.1%})")
