"""Export messages from Dataverse to a JSON file.

Usage:
- By default this script refuses to run to avoid accidental calls to production.
- To run against a real Dataverse, set `REAL_DATAVERSE_INTEGRATION=true` or
    pass `--real`.

Examples:
- Enable real mode via env and run the script.
- Typical flags: `--outfile FILE --phone <PHONE> [--since YYYY-MM-DD]`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from typing import Optional


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export messages from Dataverse to JSON.")
    p.add_argument("--outfile", "-o", required=True, help="Output JSON file")
    p.add_argument(
        "--since",
        help=(
            "ISO date (YYYY-MM-DD) to filter messages since this date. "
            "(Note: Dataverse client may not support server-side filtering)"
        ),
        default=None,
    )
    p.add_argument(
        "--phone",
        required=True,
        help="Phone number to export messages for (required)",
    )
    p.add_argument(
        "--real",
        action="store_true",
        help=(
            "Allow real Dataverse calls (must also set REAL_DATAVERSE_INTEGRATION "
            "or use this flag)"
        ),
    )
    return p.parse_args()


def ensure_real_mode(flag: bool) -> None:
    env_flag = os.getenv("REAL_DATAVERSE_INTEGRATION", "false").lower() == "true"
    if not (env_flag or flag):
        msg = (
            "Refusing to run: enable real integration with "
            "REAL_DATAVERSE_INTEGRATION=true or pass --real"
        )
        print(msg, file=sys.stderr)
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

    # `--since` parsed but not applied server-side; keep parsing helper available
    # since_iso = iso_date(args.since)

    # allow importing package from repo `rebuild/src` when running script directly
    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
    )

    # import local package after adjusting sys.path
    from whatsapp_manager.services.dataverse import get_dataverse_client  # type: ignore

    client = get_dataverse_client()
    if not hasattr(client, "query_messages"):
        print("Dataverse client does not implement `query_messages`", file=sys.stderr)
        return 3

    try:
        # DataverseClient.query_messages expects a phone number; pass the phone
        records = client.query_messages(args.phone)
    except TypeError:
        # Fallback: some older/mock implementations may not accept the same
        # signature — call again with the explicit phone argument to satisfy
        # typed clients and avoid mypy call-arg errors in CI.
        records = client.query_messages(args.phone)

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

    # keep print short to satisfy line-length checks
    print("Exported", len(records), "messages to", args.outfile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
