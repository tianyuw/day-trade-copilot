from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    alpaca_api_key: str
    alpaca_secret_key: str
    alpaca_paper: bool
    alpaca_paper_api_key: str
    alpaca_paper_secret_key: str
    alpaca_live_api_key: str | None
    alpaca_live_secret_key: str | None
    alpaca_feed: str
    alpaca_data_base_url: str
    alpaca_options_data_base_url: str
    alpaca_trading_base_url: str
    alpaca_trading_base_url_paper: str
    alpaca_trading_base_url_live: str
    alpaca_stream_url: str
    alpaca_options_stream_url: str
    alpaca_options_feed: str
    openrouter_api_key: str
    openrouter_model: str


def get_settings() -> Settings:
    env_path = Path(__file__).resolve().parents[1] / ".env"
    load_dotenv(env_path)

    import os

    alpaca_api_key = os.environ.get("ALPACA_API_KEY", "").strip()
    alpaca_secret_key = os.environ.get("ALPACA_SECRET_KEY", "").strip()
    alpaca_paper_api_key = os.environ.get("ALPACA_PAPER_API_KEY", "").strip() or alpaca_api_key
    alpaca_paper_secret_key = os.environ.get("ALPACA_PAPER_SECRET_KEY", "").strip() or alpaca_secret_key
    alpaca_live_api_key = os.environ.get("ALPACA_LIVE_API_KEY", "").strip() or None
    alpaca_live_secret_key = os.environ.get("ALPACA_LIVE_SECRET_KEY", "").strip() or None
    alpaca_paper = os.environ.get("ALPACA_PAPER", "True").strip().lower() in {"1", "true", "yes"}

    google_api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    openrouter_model = os.environ.get("OPENROUTER_MODEL", "google/gemini-3-flash-preview").strip()

    feed = os.environ.get("ALPACA_FEED", "iex").strip().lower()
    if feed not in {"iex", "sip"}:
        feed = "iex"

    data_base_url = "https://data.alpaca.markets/v2"
    options_data_base_url = "https://data.alpaca.markets/v1beta1"
    stream_url = "wss://stream.data.alpaca.markets/v2/iex" if feed == "iex" else "wss://stream.data.alpaca.markets/v2/sip"
    options_stream_url = "wss://stream.data.alpaca.markets/v1beta1/options"
    trading_base_url_paper = "https://paper-api.alpaca.markets"
    trading_base_url_live = "https://api.alpaca.markets"
    trading_base_url = trading_base_url_paper if alpaca_paper else trading_base_url_live

    options_feed = os.environ.get("ALPACA_OPTIONS_FEED", "indicative").strip().lower()
    if options_feed not in {"indicative", "opra"}:
        options_feed = "indicative"

    if not alpaca_paper_api_key or not alpaca_paper_secret_key:
        raise RuntimeError("Missing Alpaca paper API credentials in backend/.env")
    if not google_api_key:
        raise RuntimeError("Missing Google API key in backend/.env (GOOGLE_API_KEY)")

    return Settings(
        alpaca_api_key=alpaca_paper_api_key,
        alpaca_secret_key=alpaca_paper_secret_key,
        alpaca_paper=alpaca_paper,
        alpaca_paper_api_key=alpaca_paper_api_key,
        alpaca_paper_secret_key=alpaca_paper_secret_key,
        alpaca_live_api_key=alpaca_live_api_key,
        alpaca_live_secret_key=alpaca_live_secret_key,
        alpaca_feed=feed,
        alpaca_data_base_url=data_base_url,
        alpaca_options_data_base_url=options_data_base_url,
        alpaca_trading_base_url=trading_base_url,
        alpaca_trading_base_url_paper=trading_base_url_paper,
        alpaca_trading_base_url_live=trading_base_url_live,
        alpaca_stream_url=stream_url,
        alpaca_options_stream_url=options_stream_url,
        alpaca_options_feed=options_feed,
        openrouter_api_key=openrouter_api_key,
        openrouter_model=openrouter_model,
    )
