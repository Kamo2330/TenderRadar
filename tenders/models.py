from django.conf import settings
from django.db import models


class Source(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    base_url = models.URLField()
    scraper_name = models.CharField(
        max_length=100,
        help_text="Identifier used to route to a scraper implementation.",
    )
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name


class BusinessProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="business_profile"
    )
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=100, blank=True)

    def __str__(self) -> str:
        return self.company_name


class Client(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="client_profile",
    )
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=255, blank=True)
    province = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_managed = models.BooleanField(
        default=False,
        help_text="If true, TenderRadar staff applies to matched tenders on behalf of this client.",
    )

    def __str__(self) -> str:
        return self.company_name


class Tender(models.Model):
    class TenderType(models.TextChoices):
        UNKNOWN = "unknown", "Unknown / unclassified"
        SOCS = "socs", "SOCs Tenders"
        MUNICIPALITY = "municipality", "Municipality Tenders"
        UNIVERSITY = "university", "University Tenders"
        TVET_COLLEGES = "tvet_colleges", "TVET Colleges Tenders"
        PRIVATE_COMPANY = "private_company", "Private Company Tenders"
        GOVERNMENT_DEPARTMENT = "government_department", "Government Department Tenders"

    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name="tenders")
    external_id = models.CharField(
        max_length=255,
        help_text="ID from the source site to deduplicate tenders.",
    )
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True)
    department = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=255, blank=True)
    tender_type = models.CharField(
        max_length=40,
        choices=TenderType.choices,
        default=TenderType.UNKNOWN,
        db_index=True,
        help_text="High-level classification (buyer/org heuristics + API hints).",
    )
    province = models.CharField(max_length=100, blank=True)
    published_date = models.DateField(null=True, blank=True)
    closing_date = models.DateField(null=True, blank=True)
    url = models.URLField(max_length=500)
    raw_data = models.JSONField(blank=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("source", "external_id")
        ordering = ["-created_at"]

    @property
    def download_url(self) -> str:
        return self.url or ""

    def __str__(self) -> str:
        return self.title


class ClientSubscription(models.Model):
    client = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        related_name="subscription",
    )
    keywords = models.TextField(
        help_text="Comma-separated list of keywords or services (e.g. cleaning, security).",
        blank=True,
    )
    departments = models.TextField(
        blank=True,
        help_text="Comma-separated list of departments to focus on.",
    )
    provinces = models.TextField(
        blank=True,
        help_text="Comma-separated list of provinces to focus on.",
    )
    categories = models.TextField(
        blank=True,
        help_text="Comma-separated list of categories (e.g. Cleaning, Construction).",
    )
    receive_email = models.BooleanField(default=True)
    receive_telegram = models.BooleanField(default=False)
    receive_whatsapp = models.BooleanField(default=False)

    def keyword_list(self) -> list[str]:
        return [k.strip() for k in self.keywords.split(",") if k.strip()]

    def province_list(self) -> list[str]:
        return [p.strip() for p in self.provinces.split(",") if p.strip()]

    def department_list(self) -> list[str]:
        return [d.strip() for d in self.departments.split(",") if d.strip()]

    def category_list(self) -> list[str]:
        return [c.strip() for c in self.categories.split(",") if c.strip()]

    def __str__(self) -> str:
        return f"Subscription for {self.client}"


class AlertPreference(models.Model):
    FREQUENCY_IMMEDIATE = "immediate"
    FREQUENCY_DAILY = "daily"
    FREQUENCY_WEEKLY = "weekly"
    FREQUENCY_CHOICES = [
        (FREQUENCY_IMMEDIATE, "Immediate"),
        (FREQUENCY_DAILY, "Daily"),
        (FREQUENCY_WEEKLY, "Weekly"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alert_preferences"
    )
    keywords = models.TextField(
        help_text="Comma-separated list of keywords e.g. cleaning, security, IT services.",
        blank=True,
    )
    departments = models.TextField(
        blank=True,
        help_text="Comma-separated list of departments to focus on.",
    )
    provinces = models.TextField(
        blank=True,
        help_text="Comma-separated list of provinces to focus on.",
    )
    delivery_email = models.BooleanField(default=True)
    delivery_telegram = models.BooleanField(default=False)
    delivery_whatsapp = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=100, blank=True)
    whatsapp_number = models.CharField(max_length=50, blank=True)
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default=FREQUENCY_IMMEDIATE
    )

    def keyword_list(self) -> list[str]:
        return [k.strip() for k in self.keywords.split(",") if k.strip()]

    def province_list(self) -> list[str]:
        return [p.strip() for p in self.provinces.split(",") if p.strip()]

    def department_list(self) -> list[str]:
        return [d.strip() for d in self.departments.split(",") if d.strip()]

    def __str__(self) -> str:
        return f"Alert preferences for {self.user}"


class AlertEvent(models.Model):
    CHANNEL_EMAIL = "email"
    CHANNEL_TELEGRAM = "telegram"
    CHANNEL_WHATSAPP = "whatsapp"
    CHANNEL_CHOICES = [
        (CHANNEL_EMAIL, "Email"),
        (CHANNEL_TELEGRAM, "Telegram"),
        (CHANNEL_WHATSAPP, "WhatsApp"),
    ]

    STATUS_SENT = "sent"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = [
        (STATUS_SENT, "Sent"),
        (STATUS_FAILED, "Failed"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alert_events"
    )
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name="alerts")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self) -> str:
        return f"{self.channel} alert to {self.user} for {self.tender}"


class TenderApplication(models.Model):
    STATUS_NOT_SUBMITTED = "not_submitted"
    STATUS_SUBMITTED = "submitted"
    STATUS_IN_REVIEW = "in_review"
    STATUS_REJECTED = "rejected"
    STATUS_AWARDED = "awarded"
    STATUS_CHOICES = [
        (STATUS_NOT_SUBMITTED, "Not submitted"),
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_IN_REVIEW, "In review"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_AWARDED, "Awarded"),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="applications")
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=STATUS_NOT_SUBMITTED)
    submitted_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("client", "tender")
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"{self.client} -> {self.tender} ({self.status})"
