"""
URL configuration for TenderRadar project.
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from TenderRadar.drf_compat import rest_framework_available
from tenders import views as tender_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", RedirectView.as_view(url="/", permanent=False)),
    path("accounts/signup/", RedirectView.as_view(url="/", permanent=False)),
    path("accounts/logout/", tender_views.logout_view, name="logout"),
    path("", include("tenders.urls")),
]

if rest_framework_available():
    urlpatterns.insert(1, path("api/", include("tenders.api_urls")))
