from django.conf import settings
from django.core.mail import send_mail

from .models import AlertEvent, AlertPreference, ClientSubscription, Tender


def _tender_matches_preferences(tender: Tender, prefs: AlertPreference) -> bool:
    keywords = prefs.keyword_list()
    if keywords:
        haystack = f"{tender.title} {tender.description}".lower()
        if not any(keyword.lower() in haystack for keyword in keywords):
            return False

    provinces = [p.lower() for p in prefs.province_list()]
    if provinces and (tender.province or "").lower() not in provinces:
        return False

    departments = [d.lower() for d in prefs.department_list()]
    if departments and (tender.department or "").lower() not in departments:
        return False

    return True


def _tender_matches_client_subscription(tender: Tender, sub: ClientSubscription) -> bool:
    keywords = sub.keyword_list()
    if keywords:
        haystack = f"{tender.title} {tender.description}".lower()
        if not any(keyword.lower() in haystack for keyword in keywords):
            return False

    provinces = [p.lower() for p in sub.province_list()]
    if provinces and (tender.province or "").lower() not in provinces:
        return False

    departments = [d.lower() for d in sub.department_list()]
    if departments and (tender.department or "").lower() not in departments:
        return False

    categories = [c.lower() for c in sub.category_list()]
    if categories and (tender.category or "").lower() not in categories:
        return False

    return True


def notify_users_of_tender(tender: Tender) -> None:
    """
    MVP notification:
    - Existing AlertPreference-based matching (for internal users).
    - ClientSubscription-based matching (for registered clients).
    """
    # Internal user preferences
    prefs_qs = AlertPreference.objects.select_related("user")

    for prefs in prefs_qs:
        if not _tender_matches_preferences(tender, prefs):
            continue

        if prefs.delivery_email and prefs.user.email:
            _send_email_alert_to_user(tender, prefs)

    # Client subscriptions
    sub_qs = ClientSubscription.objects.select_related("client__user")

    for sub in sub_qs:
        client = sub.client
        user = client.user
        if not client.is_active or not user.is_active:
            continue

        if not _tender_matches_client_subscription(tender, sub):
            continue

        if sub.receive_email and user.email:
            _send_email_alert_to_client(tender, client)


def _build_email_lines(tender: Tender) -> list[str]:
    subject = f"New RFQ Detected: {tender.title}"
    lines = [
        "New RFQ Detected",
        "",
        f"Department: {tender.department or 'N/A'}",
        f"Service: {tender.title}",
        f"Province: {tender.province or 'N/A'}",
        f"Closing Date: {tender.closing_date or 'N/A'}",
        f"Source: {tender.source.name}",
        f"Link: {tender.url}",
    ]
    return lines


def _send_email_alert_to_user(tender: Tender, prefs: AlertPreference) -> None:
    subject = f"New RFQ Detected: {tender.title}"
    message = "\n".join(_build_email_lines(tender))

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[prefs.user.email],
            fail_silently=False,
        )
    except Exception as exc:  # noqa: BLE001
        AlertEvent.objects.create(
            user=prefs.user,
            tender=tender,
            channel=AlertEvent.CHANNEL_EMAIL,
            status=AlertEvent.STATUS_FAILED,
            error_message=str(exc),
        )
    else:
        AlertEvent.objects.create(
            user=prefs.user,
            tender=tender,
            channel=AlertEvent.CHANNEL_EMAIL,
            status=AlertEvent.STATUS_SENT,
        )


def _send_email_alert_to_client(tender: Tender, client) -> None:
    subject = f"New RFQ Detected: {tender.title}"
    message = "\n".join(_build_email_lines(tender))

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None)
    user = client.user

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as exc:  # noqa: BLE001
        AlertEvent.objects.create(
            user=user,
            tender=tender,
            channel=AlertEvent.CHANNEL_EMAIL,
            status=AlertEvent.STATUS_FAILED,
            error_message=str(exc),
        )
    else:
        AlertEvent.objects.create(
            user=user,
            tender=tender,
            channel=AlertEvent.CHANNEL_EMAIL,
            status=AlertEvent.STATUS_SENT,
        )

