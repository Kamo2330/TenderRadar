from django import forms

from .models import (
    AlertPreference,
    BusinessProfile,
    Client,
    ClientSubscription,
)


SERVICE_CHOICES = [
    ("cleaning", "Cleaning services"),
    ("security", "Security services"),
    ("construction", "Construction / building"),
    ("it_services", "IT services"),
    ("consulting", "Consulting / professional services"),
    ("catering", "Catering / food services"),
]

PROVINCE_CHOICES = [
    ("gauteng", "Gauteng"),
    ("kwa_zulu_natal", "KwaZulu-Natal"),
    ("western_cape", "Western Cape"),
    ("eastern_cape", "Eastern Cape"),
    ("free_state", "Free State"),
    ("limpopo", "Limpopo"),
    ("mpumalanga", "Mpumalanga"),
    ("north_west", "North West"),
    ("northern_cape", "Northern Cape"),
]

DEPARTMENT_CHOICES = [
    ("private_sector", "Private sector (general RFQs)"),
    ("mines", "Mines and resources"),
    ("manufacturing", "Manufacturing and industrial"),
    ("retail_fmcg", "Retail / FMCG"),
    ("construction_private", "Private construction developers"),
    ("corporate_procurement", "Corporate procurement teams"),
    ("social_development", "Department of Social Development"),
    ("health", "Department of Health"),
    ("education", "Department of Education"),
    ("public_works", "Public Works / Infrastructure"),
    ("municipal", "Municipalities"),
    ("state_owned", "State‑owned entities"),
]


class BusinessProfileForm(forms.ModelForm):
    province = forms.ChoiceField(
        choices=[("", "Select province")] + PROVINCE_CHOICES,
        required=False,
        label="Primary province",
    )

    class Meta:
        model = BusinessProfile
        fields = ["company_name", "industry", "province"]


class AlertPreferenceForm(forms.ModelForm):
    services = forms.MultipleChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Services you offer",
    )
    other_services = forms.CharField(
        required=False,
        label="Other services (comma‑separated)",
        help_text="Example: plumbing, landscaping, training",
    )
    target_provinces = forms.MultipleChoiceField(
        choices=PROVINCE_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Provinces to watch",
    )
    target_departments = forms.MultipleChoiceField(
        choices=DEPARTMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Departments to watch",
    )

    class Meta:
        model = AlertPreference
        fields = [
            "services",
            "target_departments",
            "target_provinces",
            "delivery_email",
            "delivery_telegram",
            "delivery_whatsapp",
            "frequency",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = self.instance
        if instance and instance.pk:
            # Populate choices from stored comma‑separated strings
            # Known services that match our predefined list
            known = set(k for k, _ in SERVICE_CHOICES)
            existing = instance.keyword_list()
            self.fields["services"].initial = [k for k in existing if k in known]
            # Anything else goes into "other_services"
            other = [k for k in existing if k not in known]
            if other:
                self.fields["other_services"].initial = ", ".join(other)
            self.fields["target_provinces"].initial = instance.province_list()
            self.fields["target_departments"].initial = instance.department_list()

    def save(self, commit: bool = True):
        obj: AlertPreference = super().save(commit=False)

        services = self.cleaned_data.get("services") or []
        extra = self.cleaned_data.get("other_services") or ""
        extra_list = [e.strip() for e in extra.split(",") if e.strip()]
        provinces = self.cleaned_data.get("target_provinces") or []
        departments = self.cleaned_data.get("target_departments") or []

        # Combine predefined and custom services into one keyword string
        all_services = services + extra_list
        obj.keywords = ", ".join(all_services)
        obj.provinces = ", ".join(provinces)
        obj.departments = ", ".join(departments)

        if commit:
            obj.save()
        return obj


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            "company_name",
            "contact_person",
            "email",
            "phone",
            "industry",
            "province",
            "is_active",
            "is_managed",
        ]


class ClientSubscriptionForm(forms.ModelForm):
    class Meta:
        model = ClientSubscription
        fields = [
            "keywords",
            "departments",
            "provinces",
            "categories",
            "receive_email",
            "receive_telegram",
            "receive_whatsapp",
        ]

