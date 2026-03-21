"""
Aggregator API: Tenders-SA (third-party). Includes RFQs from many organisations,
including SOEs and corporate-style notices.

Respect their rate limits (e.g. ~60 req/min). We paginate with modest page sizes.

API base observed: https://www.tenders-sa.org/api/tenders
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Optional

from .base import BaseScraper
from .http_client import fetch_json
from .tender_type_classifier import classify_tender_type

API_BASE = "https://www.tenders-sa.org/api/tenders"
FALLBACK_URL = "https://www.tenders-sa.org/"


def _parse_iso_date(value: Optional[str]) -> Optional[date]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except (ValueError, TypeError):
        return None


def _safe_url(u: Optional[str], max_len: int = 500) -> str:
    if not u:
        return FALLBACK_URL
    u = u.strip()
    return u if len(u) <= max_len else FALLBACK_URL


def _record_to_item(row: dict[str, Any]) -> Dict[str, Any]:
    tender_id = str(row.get("tender_id") or row.get("id") or "")
    external_id = f"tsa-{tender_id}" if tender_id else f"tsa-{row.get('id', 'unknown')}"

    title = (row.get("title") or "Untitled").strip()[:500]
    description = (row.get("description") or "").strip()
    org = row.get("sourceOrganization") or ""
    dept = org[:255] if org else ""

    org_type = ""
    info = row.get("organizationInfo") or {}
    if isinstance(info, dict):
        org_type = (info.get("type") or "").strip()
        if info.get("name") and not dept:
            dept = str(info.get("name"))[:255]

    classified_type = classify_tender_type(
        buyer_or_org_name=dept,
        title=title,
        organization_api_type=org_type or None,
    )

    province = (row.get("province") or "").strip()[:100]
    notice_type = (row.get("type") or "").strip()
    category = notice_type[:255] if notice_type else ""

    closing_date = _parse_iso_date(row.get("closingDate"))
    published_date = _parse_iso_date(row.get("createdAt"))

    docs: List[dict] = row.get("requiredDocuments") or []
    url = FALLBACK_URL
    for d in docs:
        u = d.get("url") if isinstance(d, dict) else None
        if u:
            url = _safe_url(u)
            break

    return {
        "external_id": external_id[:255],
        "title": title,
        "description": description,
        "department": dept,
        "category": category,
        "tender_type": classified_type,
        "province": province,
        "published_date": published_date,
        "closing_date": closing_date,
        "url": url,
        "raw_data": {
            "source": "tenders-sa.org",
            "reference_number": row.get("referenceNumber"),
            "organization_type": org_type,
            "tender_type_classified": classified_type,
            "notice_type": notice_type,
        },
    }


class TendersSAScraper(BaseScraper):
    source_slug = "tenders_sa"

    def __init__(
        self,
        *,
        max_pages: int = 20,
        page_size: int = 50,
    ) -> None:
        self.max_pages = max(1, max_pages)
        self.page_size = min(100, max(1, page_size))

    def fetch_tenders(self) -> Iterable[Dict[str, Any]]:
        for page in range(1, self.max_pages + 1):
            url = f"{API_BASE}?page={page}&limit={self.page_size}"
            try:
                data = fetch_json(url)
            except Exception:
                break

            tenders = data.get("tenders") or []
            if not tenders:
                break

            for row in tenders:
                if isinstance(row, dict):
                    yield _record_to_item(row)

            pagination = data.get("pagination") or {}
            total_pages = pagination.get("pages")
            if total_pages and page >= int(total_pages):
                break
