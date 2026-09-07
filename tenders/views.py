from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.utils import OperationalError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AlertPreferenceForm,
    BusinessProfileForm,
    ClientForm,
    ClientSubscriptionForm,
    PROVINCE_CHOICES,
)
from django.db.models import Count, Q
from django.utils import timezone as dj_timezone
from datetime import timedelta

from .models import (
    AlertPreference,
    BusinessProfile,
    Client,
    ClientSubscription,
    Tender,
    TenderApplication,
)
from .tender_queryset import filter_tenders

User = get_user_model()


def logout_view(request):
    if request.method in ("POST", "GET"):
        logout(request)
    return redirect("tenders:dashboard")


def staff_required(view_func):
    decorated = login_required(user_passes_test(lambda u: u.is_staff)(view_func))
    return decorated


def health_check(request):
    """Plain-text check — if you see this, you hit the real TenderRadar server."""
    import django

    return HttpResponse(
        "TENDERRADAR OK\n"
        f"Django {django.get_version()}\n"
        "Open: http://127.0.0.1:8765/\n",
        content_type="text/plain",
    )


def dashboard(request):
    """Public tender dashboard — no login required."""
    q = request.GET.get("q", "").strip()
    tender_type = request.GET.get("tender_type", "").strip()
    province = request.GET.get("province", "").strip()
    source = request.GET.get("source", "").strip()
    sort = request.GET.get("sort", "newest").strip() or "newest"

    try:
        tenders_qs = filter_tenders(
            q=q,
            tender_type=tender_type,
            province=province,
            source=source,
            date_filter="open",
            sort=sort,
        )
        total_count = tenders_qs.count()
        source_count = (
            Tender.objects.values("source_id").distinct().count()
        )
        paginator = Paginator(tenders_qs, 25)
        page_obj = paginator.get_page(request.GET.get("page"))
        tenders = list(page_obj.object_list)
    except OperationalError:
        tenders = []
        page_obj = None
        total_count = 0
        source_count = 0

    context = {
        "tenders": tenders,
        "page_obj": page_obj,
        "q": q,
        "tender_type": tender_type,
        "province": province,
        "source": source,
        "sort": sort,
        "total_count": total_count,
        "source_count": source_count,
        "tender_type_options": Tender.TenderType.choices,
        "province_options": (
            Tender.objects.exclude(province="")
            .values_list("province", flat=True)
            .distinct()
            .order_by("province")
        ),
        "source_options": (
            Tender.objects.values_list("source__slug", "source__name")
            .distinct()
            .order_by("source__name")
        ),
    }
    return render(request, "tenders/dashboard.html", context)


@login_required
def preferences(request):
    # Staff preferences = managed clients overview
    if request.user.is_staff:
        return redirect("tenders:staff_managed_overview")
    try:
        profile, _ = BusinessProfile.objects.get_or_create(
            user=request.user, defaults={"company_name": ""}
        )
        prefs, _ = AlertPreference.objects.get_or_create(user=request.user)
    except OperationalError:
        # Database tables for profiles/preferences not created yet
        return render(
            request,
            "tenders/preferences.html",
            {
                "profile_form": None,
                "prefs_form": None,
                "db_error": True,
            },
        )

    if request.method == "POST":
        profile_form = BusinessProfileForm(request.POST, instance=profile)
        prefs_form = AlertPreferenceForm(request.POST, instance=prefs)
        if profile_form.is_valid() and prefs_form.is_valid():
            profile_form.save()
            prefs_form.save()
            return redirect(reverse("tenders:dashboard"))
    else:
        profile_form = BusinessProfileForm(instance=profile)
        prefs_form = AlertPreferenceForm(instance=prefs)

    context = {
        "profile_form": profile_form,
        "prefs_form": prefs_form,
        "db_error": False,
    }
    return render(request, "tenders/preferences.html", context)


@staff_required
def staff_client_list(request):
    try:
        clients = Client.objects.select_related("user").all()

        q = request.GET.get("q", "").strip()
        province = request.GET.get("province", "").strip()
        sort = request.GET.get("sort", "name")

        if q:
            clients = clients.filter(company_name__icontains=q)

        if province:
            clients = clients.filter(province__iexact=province)

        if sort == "name":
            clients = clients.order_by("company_name")
        elif sort == "recent":
            clients = clients.order_by("-id")
        else:
            clients = clients.order_by("company_name")

    except OperationalError:
        clients = []

    province_options = [("", "All provinces")] + PROVINCE_CHOICES

    return render(
        request,
        "tenders/staff/client_list.html",
        {
            "clients": clients,
            "q": q,
            "province": province,
            "sort": sort,
            "province_options": province_options,
        },
    )


@staff_required
def staff_client_create(request):
    """
    Staff capture flow:
    - Create a Django user account for the client (username=email).
    - Create a Client record.
    - Create/update ClientSubscription for matching tenders.
    """
    user_form_errors = None

    if request.method == "POST":
        client_form = ClientForm(request.POST)
        sub_form = ClientSubscriptionForm(request.POST)

        if client_form.is_valid() and sub_form.is_valid():
            email = client_form.cleaned_data["email"]
            username = email

            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "is_active": True,
                },
            )

            client = client_form.save(commit=False)
            client.user = user
            client.save()

            subscription, _ = ClientSubscription.objects.get_or_create(client=client)
            for field in ClientSubscriptionForm.Meta.fields:
                setattr(subscription, field, sub_form.cleaned_data.get(field))
            subscription.save()

            return redirect("tenders:staff_client_list")
    else:
        client_form = ClientForm()
        sub_form = ClientSubscriptionForm()

    return render(
        request,
        "tenders/staff/client_form.html",
        {
            "client_form": client_form,
            "sub_form": sub_form,
            "user_form_errors": user_form_errors,
        },
    )


def _client_matched_tenders_queryset(client: Client):
    """
    Build a queryset of tenders that match a client's subscription.
    This is a simple MVP matcher (title/description keyword contains + exact filters).
    """
    try:
        sub = client.subscription
    except Exception:  # noqa: BLE001
        return Tender.objects.none()

    qs = Tender.objects.all()

    keywords = sub.keyword_list()
    if keywords:
        keyword_q = Q()
        for kw in keywords:
            keyword_q |= Q(title__icontains=kw) | Q(description__icontains=kw)
        qs = qs.filter(keyword_q)

    provinces = sub.province_list()
    if provinces:
        prov_q = Q()
        for p in provinces:
            prov_q |= Q(province__iexact=p)
        qs = qs.filter(prov_q)

    departments = sub.department_list()
    if departments:
        dep_q = Q()
        for d in departments:
            dep_q |= Q(department__iexact=d)
        qs = qs.filter(dep_q)

    categories = sub.category_list()
    if categories:
        cat_q = Q()
        for c in categories:
            cat_q |= Q(category__iexact=c)
        qs = qs.filter(cat_q)

    return qs


@login_required
def client_tenders(request):
    """
    Client portal: show only tenders that match this client's profile.
    """
    try:
        client = request.user.client_profile
    except Client.DoesNotExist:  # type: ignore[attr-defined]
        return redirect("tenders:dashboard")
    except Exception:  # noqa: BLE001
        return redirect("tenders:dashboard")

    days = int(request.GET.get("days", "30") or "30")
    since = dj_timezone.now().date() - timedelta(days=days)

    try:
        matched_qs = (
            _client_matched_tenders_queryset(client)
            .filter(closing_date__gte=since)
            .order_by("closing_date")[:200]
        )
        matched = list(matched_qs)

        existing = {
            ta.tender_id: ta
            for ta in TenderApplication.objects.filter(client=client, tender__in=matched)
        }
    except OperationalError:
        matched = []
        existing = {}

    items = []
    for tender in matched:
        ta = existing.get(tender.id)
        status = ta.status if ta else TenderApplication.STATUS_NOT_SUBMITTED
        items.append({"tender": tender, "status": status})

    return render(
        request,
        "tenders/client/tenders.html",
        {"client": client, "items": items, "days": days, "since": since},
    )


@login_required
def client_apply(request, tender_id: int):
    """
    Client clicks 'Apply' on a tender – create or update TenderApplication.
    """
    if request.method != "POST":
        return redirect("tenders:client_tenders")

    try:
        client = request.user.client_profile
    except Exception:  # noqa: BLE001
        return redirect("tenders:dashboard")

    try:
        tender = Tender.objects.get(id=tender_id)
    except Tender.DoesNotExist:
        return redirect("tenders:client_tenders")

    ta, _ = TenderApplication.objects.get_or_create(client=client, tender=tender)
    ta.status = TenderApplication.STATUS_SUBMITTED
    ta.submitted_at = dj_timezone.now()
    ta.save()

    return redirect("tenders:client_tenders")


@staff_required
def staff_managed_overview(request):
    """
    Staff dashboard showing coverage status for managed (paying) clients.
    """
    window_days = int(request.GET.get("days", "30") or "30")
    since = dj_timezone.now().date() - timedelta(days=window_days)

    try:
        managed_clients = (
            Client.objects.select_related("user")
            .filter(is_managed=True, is_active=True, user__is_active=True)
            .order_by("company_name")
        )

        rows = []
        total_clients = 0
        up_to_date = 0
        pending_clients = 0

        for client in managed_clients:
            total_clients += 1
            matched_qs = _client_matched_tenders_queryset(client).filter(created_at__date__gte=since)
            matched_ids = list(matched_qs.values_list("id", flat=True))
            matched_count = len(matched_ids)

            submitted_count = TenderApplication.objects.filter(
                client=client,
                tender_id__in=matched_ids,
                status__in=[TenderApplication.STATUS_SUBMITTED, TenderApplication.STATUS_IN_REVIEW, TenderApplication.STATUS_AWARDED],
            ).count()

            pending_count = max(matched_count - submitted_count, 0)

            if pending_count == 0 and matched_count > 0:
                up_to_date += 1
            if pending_count > 0:
                pending_clients += 1

            rows.append(
                {
                    "client": client,
                    "matched": matched_count,
                    "submitted": submitted_count,
                    "pending": pending_count,
                }
            )

    except OperationalError:
        rows = []
        total_clients = 0
        up_to_date = 0
        pending_clients = 0
        window_days = 30

    return render(
        request,
        "tenders/staff/managed_overview.html",
        {
            "rows": rows,
            "window_days": window_days,
            "total_clients": total_clients,
            "up_to_date": up_to_date,
            "pending_clients": pending_clients,
        },
    )


@staff_required
def staff_client_coverage_detail(request, client_id: int):
    """
    Drill-down for one managed client: show matched tenders and application status,
    with a simple action to mark as submitted.
    """
    client = Client.objects.select_related("user").get(id=client_id)
    if not client.is_managed:
        return redirect("tenders:staff_managed_overview")

    days = int(request.GET.get("days", "30") or "30")
    since = dj_timezone.now().date() - timedelta(days=days)

    try:
        matched_qs = _client_matched_tenders_queryset(client).filter(created_at__date__gte=since).order_by("-created_at")[:200]
        matched = list(matched_qs)

        existing = {
            ta.tender_id: ta
            for ta in TenderApplication.objects.filter(client=client, tender__in=matched)
        }

        if request.method == "POST":
            tender_id = int(request.POST.get("tender_id"))
            action = request.POST.get("action")

            tender = Tender.objects.get(id=tender_id)
            ta, _ = TenderApplication.objects.get_or_create(client=client, tender=tender)

            if action == "mark_submitted":
                ta.status = TenderApplication.STATUS_SUBMITTED
                ta.submitted_at = dj_timezone.now()
                ta.save()

            return redirect(reverse("tenders:staff_client_coverage_detail", kwargs={"client_id": client.id}) + f"?days={days}")

    except OperationalError:
        matched = []
        existing = {}

    items = []
    for tender in matched:
        ta = existing.get(tender.id)
        status = ta.status if ta else TenderApplication.STATUS_NOT_SUBMITTED
        items.append({"tender": tender, "status": status, "ta": ta})

    return render(
        request,
        "tenders/staff/client_coverage_detail.html",
        {"client": client, "items": items, "days": days, "since": since},
    )


@staff_required
def staff_applications_queue(request):
    """
    Staff view: list of tenders that clients want us to apply for.
    """
    status_filter = request.GET.get("status", "submitted")

    try:
        qs = TenderApplication.objects.select_related("client", "tender").filter(
            client__is_managed=True
        )
        if status_filter:
            qs = qs.filter(status=status_filter)

        qs = qs.order_by("-updated_at")[:200]
        applications = list(qs)
    except OperationalError:
        applications = []

    return render(
        request,
        "tenders/staff/applications_queue.html",
        {"applications": applications, "status_filter": status_filter},
    )

