"""Minimal JSON HTTP client (stdlib only)."""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request
from typing import Any

DEFAULT_TIMEOUT = 60
USER_AGENT = "TenderRadar/1.0 (+https://github.com/) compatible; procurement aggregator"


def fetch_json(url: str, timeout: int = DEFAULT_TIMEOUT) -> dict[str, Any]:
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="GET",
    )
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    return json.loads(raw)
