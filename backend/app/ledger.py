from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class LedgerConfig:
    db_path: Path


class Ledger:
    def __init__(self, config: LedgerConfig | None = None) -> None:
        if config is None:
            db_path = Path(__file__).resolve().parents[1] / "trades.db"
            config = LedgerConfig(db_path=db_path)
        self._config = config

    def _connect(self) -> sqlite3.Connection:
        self._config.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self._config.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def ensure_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trades (
                  trade_id TEXT PRIMARY KEY,
                  symbol TEXT NOT NULL,
                  mode TEXT NOT NULL,
                  execution TEXT NOT NULL,
                  state TEXT,
                  option_symbol TEXT,
                  option_right TEXT,
                  option_expiration TEXT,
                  option_strike REAL,
                  contracts_total INTEGER,
                  contracts_remaining INTEGER,
                  entry_time TEXT,
                  entry_premium REAL,
                  exit_time TEXT,
                  exit_premium REAL,
                  pnl_option_usd REAL,
                  extra_json TEXT,
                  created_at TEXT NOT NULL,
                  updated_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS trade_events (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  trade_id TEXT NOT NULL,
                  symbol TEXT,
                  timestamp TEXT NOT NULL,
                  event_type TEXT NOT NULL,
                  analysis_id TEXT,
                  bar_time TEXT,
                  payload_json TEXT
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trade_events_trade_id ON trade_events(trade_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trade_events_ts ON trade_events(timestamp)")

            def has_column(table: str, col: str) -> bool:
                rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
                return any(str(r["name"]) == col for r in rows)

            if not has_column("trades", "state"):
                conn.execute("ALTER TABLE trades ADD COLUMN state TEXT")
            if not has_column("trade_events", "symbol"):
                conn.execute("ALTER TABLE trade_events ADD COLUMN symbol TEXT")

            if has_column("trade_events", "symbol"):
                conn.execute("CREATE INDEX IF NOT EXISTS idx_trade_events_symbol_ts ON trade_events(symbol, timestamp)")

    def upsert_trade(self, trade: dict[str, Any]) -> None:
        now = _utc_now_iso()
        trade_id = str(trade.get("trade_id") or "").strip()
        symbol = str(trade.get("symbol") or "").strip().upper()
        mode = str(trade.get("mode") or "realtime").strip().lower()
        execution = str(trade.get("execution") or "paper").strip().lower()
        state = str(trade.get("state") or "").strip().upper() or None
        if not trade_id or not symbol:
            raise ValueError("trade_id and symbol are required")

        extra = dict(trade.get("extra") or {})
        extra_json = json.dumps(extra, ensure_ascii=False) if extra else None

        with self._connect() as conn:
            row = conn.execute("SELECT trade_id FROM trades WHERE trade_id = ?", (trade_id,)).fetchone()
            created_at = now if row is None else None

            conn.execute(
                """
                INSERT INTO trades (
                  trade_id, symbol, mode, execution, state,
                  option_symbol, option_right, option_expiration, option_strike,
                  contracts_total, contracts_remaining,
                  entry_time, entry_premium, exit_time, exit_premium, pnl_option_usd,
                  extra_json, created_at, updated_at
                ) VALUES (
                  :trade_id, :symbol, :mode, :execution, :state,
                  :option_symbol, :option_right, :option_expiration, :option_strike,
                  :contracts_total, :contracts_remaining,
                  :entry_time, :entry_premium, :exit_time, :exit_premium, :pnl_option_usd,
                  :extra_json, :created_at, :updated_at
                )
                ON CONFLICT(trade_id) DO UPDATE SET
                  symbol=excluded.symbol,
                  mode=excluded.mode,
                  execution=excluded.execution,
                  state=COALESCE(excluded.state, trades.state),
                  option_symbol=COALESCE(excluded.option_symbol, trades.option_symbol),
                  option_right=COALESCE(excluded.option_right, trades.option_right),
                  option_expiration=COALESCE(excluded.option_expiration, trades.option_expiration),
                  option_strike=COALESCE(excluded.option_strike, trades.option_strike),
                  contracts_total=COALESCE(excluded.contracts_total, trades.contracts_total),
                  contracts_remaining=COALESCE(excluded.contracts_remaining, trades.contracts_remaining),
                  entry_time=COALESCE(excluded.entry_time, trades.entry_time),
                  entry_premium=COALESCE(excluded.entry_premium, trades.entry_premium),
                  exit_time=COALESCE(excluded.exit_time, trades.exit_time),
                  exit_premium=COALESCE(excluded.exit_premium, trades.exit_premium),
                  pnl_option_usd=COALESCE(excluded.pnl_option_usd, trades.pnl_option_usd),
                  extra_json=COALESCE(excluded.extra_json, trades.extra_json),
                  updated_at=excluded.updated_at
                """,
                {
                    "trade_id": trade_id,
                    "symbol": symbol,
                    "mode": mode,
                    "execution": execution,
                    "state": state,
                    "option_symbol": trade.get("option_symbol"),
                    "option_right": trade.get("option_right"),
                    "option_expiration": trade.get("option_expiration"),
                    "option_strike": trade.get("option_strike"),
                    "contracts_total": trade.get("contracts_total"),
                    "contracts_remaining": trade.get("contracts_remaining"),
                    "entry_time": trade.get("entry_time"),
                    "entry_premium": trade.get("entry_premium"),
                    "exit_time": trade.get("exit_time"),
                    "exit_premium": trade.get("exit_premium"),
                    "pnl_option_usd": trade.get("pnl_option_usd"),
                    "extra_json": extra_json,
                    "created_at": created_at or now,
                    "updated_at": now,
                },
            )

    def append_event(
        self,
        trade_id: str,
        event_type: str,
        symbol: str | None = None,
        timestamp: str | None = None,
        analysis_id: str | None = None,
        bar_time: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        trade_id = str(trade_id or "").strip()
        event_type = str(event_type or "").strip()
        if not trade_id or not event_type:
            raise ValueError("trade_id and event_type are required")
        ts = timestamp or _utc_now_iso()
        sym = str(symbol or "").strip().upper() or None
        payload_json = json.dumps(payload, ensure_ascii=False) if payload is not None else None
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO trade_events (trade_id, symbol, timestamp, event_type, analysis_id, bar_time, payload_json)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (trade_id, sym, ts, event_type, analysis_id, bar_time, payload_json),
            )

    def list_trades(
        self,
        symbol: str | None = None,
        mode: str | None = None,
        execution: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        q = "SELECT * FROM trades"
        where: list[str] = []
        args: list[Any] = []
        if symbol:
            where.append("symbol = ?")
            args.append(symbol.strip().upper())
        if mode:
            where.append("mode = ?")
            args.append(mode.strip().lower())
        if execution:
            where.append("execution = ?")
            args.append(execution.strip().lower())
        if where:
            q += " WHERE " + " AND ".join(where)
        q += " ORDER BY updated_at DESC LIMIT ?"
        args.append(int(limit))
        with self._connect() as conn:
            rows = conn.execute(q, args).fetchall()
            return [dict(r) for r in rows]

    def get_trade(self, trade_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM trades WHERE trade_id = ?", (trade_id,)).fetchone()
            return dict(row) if row else None

    def list_events(self, trade_id: str, limit: int = 500) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM trade_events WHERE trade_id = ? ORDER BY id ASC LIMIT ?",
                (trade_id, int(limit)),
            ).fetchall()
            return [dict(r) for r in rows]

    def list_events_by_symbol(
        self,
        symbol: str,
        *,
        since_ts: str | None = None,
        limit: int = 500,
        event_types: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        sym = symbol.strip().upper()
        if not sym:
            return []
        q = """
            SELECT
              e.*,
              COALESCE(e.symbol, t.symbol) AS resolved_symbol
            FROM trade_events e
            LEFT JOIN trades t ON t.trade_id = e.trade_id
            WHERE COALESCE(e.symbol, t.symbol) = ?
        """
        args: list[Any] = [sym]
        if since_ts:
            q += " AND e.timestamp >= ?"
            args.append(since_ts)
        if event_types:
            q += " AND e.event_type IN (" + ",".join("?" for _ in event_types) + ")"
            args.extend([str(x) for x in event_types])
        q += " ORDER BY e.timestamp ASC, e.id ASC LIMIT ?"
        args.append(int(limit))
        with self._connect() as conn:
            rows = conn.execute(q, args).fetchall()
            out: list[dict[str, Any]] = []
            for r in rows:
                d = dict(r)
                d["symbol"] = d.pop("resolved_symbol", d.get("symbol"))
                out.append(d)
            return out

    def get_active_trades(self, symbols: list[str]) -> list[dict[str, Any]]:
        syms = [s.strip().upper() for s in symbols if s and s.strip()]
        if not syms:
            return []
        q = (
            "SELECT * FROM trades WHERE symbol IN ("
            + ",".join("?" for _ in syms)
            + ") AND COALESCE(contracts_remaining, 0) > 0 AND (exit_time IS NULL OR exit_time = '') ORDER BY updated_at DESC"
        )
        with self._connect() as conn:
            rows = conn.execute(q, syms).fetchall()
            return [dict(r) for r in rows]
