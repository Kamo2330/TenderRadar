"""
Classify tenders into high-level TenderRadar types from buyer/org text.
Heuristic only — not perfect; stored value can be refined later.
"""

from __future__ import annotations

import re
from typing import Optional

SOC_KEYWORDS = (
    "eskom",
    "transnet",
    "sanral",
    "prasa",
    "sabc",
    "denel",
    "csir",
    "safcol",
    "sanparks",
    "armscor",
    "broadband infraco",
    "rand water",
    "johannesburg water",
    "city power",
    "portnet",
    "transnet freight",
    "transnet national",
    "south african express",
    "land bank",
    "landbank",
    "development bank of southern africa",
    "db sa",
    "petro sa",
    "petrosa",
    "alexkor",
    "deneb",
    "south african forestry",
    "passenger rail",
    "airports company",
    "acsal",
    "telkom",
    "sentech",
)


def classify_tender_type(
    *,
    buyer_or_org_name: str = "",
    title: str = "",
    organization_api_type: Optional[str] = None,
) -> str:
    """Return Tender.TenderType database value (slug string)."""
    from tenders.models import Tender

    text = f"{buyer_or_org_name} {title}".lower()
    api_t = (organization_api_type or "").strip().upper()
    TT = Tender.TenderType

    # TVET / colleges (before "university" false positives)
    if re.search(
        r"\btvet\b|technical\s+and\s+vocational|fet\s+college|tvet\s+college",
        text,
    ):
        return TT.TVET_COLLEGES.value

    if "university" in text or "universiteit" in text:
        return TT.UNIVERSITY.value

    if re.search(
        r"municipality|metropolitan|metro\s+police|local\s+municipality|district\s+municipal",
        text,
    ):
        return TT.MUNICIPALITY.value

    if "department of" in text or re.search(
        r"\b(national|provincial)\s+department\b", text
    ):
        return TT.GOVERNMENT_DEPARTMENT.value

    for kw in SOC_KEYWORDS:
        if kw in text:
            return TT.SOCS.value

    if api_t in ("PRIVATE", "COMMERCIAL", "CORPORATE"):
        return TT.PRIVATE_COMPANY.value

    if re.search(
        r"\(pty\)|\bpty\b|proprietary\s+limited|proprietary\s+ltd|\bltd\b|\bcc\b|close corporation",
        text,
    ):
        return TT.PRIVATE_COMPANY.value

    if api_t == "GOVERNMENT":
        # Could be dept, municipality, or SOC — text rules above already ran
        return TT.GOVERNMENT_DEPARTMENT.value

    return TT.UNKNOWN.value
