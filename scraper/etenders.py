"""
Real scraper for South African national eTenders using the official OCDS API.

API docs: https://ocds-api.etenders.gov.za/swagger/
Terms: https://data.etenders.gov.za/Home/LearnMore

The API requires both dateFrom and dateTo (YYYY-MM-DD).
"""

from __future__ import annotations

import json
import urllib.error
from datetime import date, datetime, timedelta
from typing import Any, Dict, Iterable, Optional

from .base import BaseScraper
from .http_client import fetch_json
from .tender_type_classifier import classify_tender_type

OCDS_BASE = "https://ocds-api.etenders.gov.za/api/OCDSReleases"
PORTAL_FALLBACK = "https://www.etenders.gov.za/"


def _parse_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except (ValueError, TypeError):
        return None


def _safe_url(u: Optional[str], fallback: str, max_len: int = 500) -> str:
    if not u:
        return fallback
    u = u.strip()
    if len(u) <= max_len:
        return u
    return fallback


def _release_to_item(release: dict[str, Any]) -> Optional[Dict[str, Any]]:
    ocid = release.get("ocid")
    if not ocid:
        return None

    tender = release.get("tender") or {}
    if not tender:
        return None

    title = (tender.get("title") or ocid).strip()
    description = (tender.get("description") or "").strip()

    buyer = release.get("buyer") or {}
    department = (buyer.get("name") or "").strip()
    procuring = tender.get("procuringEntity") or {}
    if not department:
        department = (procuring.get("name") or "").strip()

    province = (tender.get("province") or "").strip()
    category = (
        tender.get("category")
        or tender.get("mainProcurementCategory")
        or ""
    )
    if isinstance(category, str):
        category = category.strip()
    else:
        category = str(category) if category else ""

    tp = tender.get("tenderPeriod") or {}
    closing_date = _parse_date(tp.get("endDate"))
    published_date = _parse_date(release.get("date")) or _parse_date(tp.get("startDate"))

    url = PORTAL_FALLBACK
    for doc in tender.get("documents") or []:
        u = doc.get("url")
        if u:
            url = _safe_url(u, PORTAL_FALLBACK)
            break

    tender_type = classify_tender_type(
        buyer_or_org_name=department,
        title=title,
        organization_api_type=None,
    )

    return {
        "external_id": str(ocid)[:255],
        "title": title[:500],
        "description": description,
        "department": department[:255],
        "category": category[:255] if category else "",
        "tender_type": tender_type,
        "province": province[:100],
        "published_date": published_date,
        "closing_date": closing_date,
        "url": url,
        "raw_data": {
            "ocid": ocid,
            "release_id": release.get("id"),
            "source": "ocds-api.etenders.gov.za",
            "tender_status": tender.get("status"),
            "tender_type_classified": tender_type,
        },
    }


class EtendersScraper(BaseScraper):
    """Fetches releases from the National Treasury OCDS API."""

    source_slug = "etenders"

    def __init__(
        self,
        *,
        days_back: int = 14,
        max_pages: int = 50,
        page_size: int = 100,
    ) -> None:
        self.days_back = max(1, days_back)
        self.max_pages = max(1, max_pages)
        self.page_size = min(1000, max(1, page_size))

    def fetch_tenders(self) -> Iterable[Dict[str, Any]]:
        end = date.today()
        start = end - timedelta(days=self.days_back)

        date_from = start.isoformat()
        date_to = end.isoformat()

        next_url: Optional[str] = (
            f"{OCDS_BASE}?PageNumber=1&PageSize={self.page_size}"
            f"&dateFrom={date_from}&dateTo={date_to}"
        )
        pages = 0

        while next_url and pages < self.max_pages:
            pages += 1
            try:
                data = fetch_json(next_url)
            except (
                urllib.error.URLError,
                urllib.error.HTTPError,
                OSError,
                json.JSONDecodeError,
                ValueError,
            ):
                break

            releases = data.get("releases") or []
            for release in releases:
                item = _release_to_item(release)
                if item:
                    yield item

            links = data.get("links") or {}
            next_url = links.get("next")
            if not releases:
                break
