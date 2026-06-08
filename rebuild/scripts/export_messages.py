"""Export messages from Dataverse to a JSON file.

Usage:
  - By default this script refuses to run to avoid accidental calls to production.
  - To run against a real Dataverse, set environment variable
    `REAL_DATAVERSE_INTEGRATION=true` or pass `--real`.

Examples:
  REAL_DATAVERSE_INTEGRATION=true python scripts/export_messages.py --outfile messages.json
  python scripts/export_messages.py --real --since 2026-01-01 --outfile out.json
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from whatsapp_manager.services.dataverse import get_dataverse_client  # type: ignore


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export messages from Dataverse to JSON.")
    p.add_argument("--outfile", "-o", required=True, help="Output JSON file")
    p.add_argument(
        "--since",
        help="ISO date (YYYY-MM-DD) to filter messages since this date",
        default=None,
    )
    p.add_argument(
        "--real",
        action="store_true",
        help="Allow real Dataverse calls (must also set REAL_DATAVERSE_INTEGRATION or use this flag)",
    )
    return p.parse_args()


def ensure_real_mode(flag: bool) -> None:
    env_flag = os.getenv("REAL_DATAVERSE_INTEGRATION", "false").lower() == "true"
    if not (env_flag or flag):
        print(
            "Refusing to run: enable real integration with REAL_DATAVERSE_INTEGRATION=true or pass --real",
            file=sys.stderr,
        )
        sys.exit(2)


def iso_date(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    try:
        d = datetime.fromisoformat(s)
        return d.isoformat()
    except ValueError:
        try:
            d = datetime.strptime(s, "%Y-%m-%d")
            return d.isoformat()
        except Exception:
            raise


def main() -> int:
    args = parse_args()
    ensure_real_mode(args.real)

    since_iso = iso_date(args.since)

    client = get_dataverse_client()
    if not hasattr(client, "query_messages"):
        print("Dataverse client does not implement `query_messages`", file=sys.stderr)
        return 3

    try:
        # `query_messages` should accept an optional `since` parameter; adapt if your client differs.
        records: List[Dict[str, Any]] = client.query_messages(since=since_iso)  # type: ignore[arg-type]
    except TypeError:
        # fallback call without since
        records = client.query_messages()

    # Normalize to list
    if records is None:
        records = []

    with open(args.outfile, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "exported_at": datetime.utcnow().isoformat(),
                "count": len(records),
                "items": records,
            },
            fh,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Exported {len(records)} messages to {args.outfile}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
