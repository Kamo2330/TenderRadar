from datetime import timedelta

from django.db.models import Q
from django.utils import timezone

from .models import Tender


def filter_tenders(
    *,
    q: str = "",
    tender_type: str = "",
    province: str = "",
    source: str = "",
    date_filter: str = "open",
    sort: str = "newest",
):
    """Shared tender list filtering for dashboard views."""
    today = timezone.localdate()
    tenders_qs = Tender.objects.select_related("source").all()

    if q:
        terms = [x for x in q.split() if x]
        smart_q = Q()
        for term in terms:
            smart_q &= (
                Q(title__icontains=term)
                | Q(description__icontains=term)
                | Q(department__icontains=term)
                | Q(category__icontains=term)
            )
        tenders_qs = tenders_qs.filter(smart_q)

    if tender_type:
        tenders_qs = tenders_qs.filter(tender_type=tender_type)
    if province:
        tenders_qs = tenders_qs.filter(province__iexact=province)
    if source:
        tenders_qs = tenders_qs.filter(source__slug=source)

    if date_filter == "open":
        tenders_qs = tenders_qs.filter(closing_date__gte=today)
    elif date_filter == "closing_7":
        tenders_qs = tenders_qs.filter(
            closing_date__gte=today,
            closing_date__lte=today + timedelta(days=7),
        )
    elif date_filter == "expired":
        tenders_qs = tenders_qs.filter(closing_date__lt=today)

    if sort == "closing_soon":
        tenders_qs = tenders_qs.order_by("closing_date", "-created_at")
    elif sort == "closing_latest":
        tenders_qs = tenders_qs.order_by("-closing_date", "-created_at")
    else:
        tenders_qs = tenders_qs.order_by("-created_at")

    return tenders_qs
