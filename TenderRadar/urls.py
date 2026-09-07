"""
URL configuration for TenderRadar project.
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from tenders import views as tender_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tenders.api_urls")),
    path("accounts/login/", RedirectView.as_view(url="/", permanent=False)),
    path("accounts/signup/", RedirectView.as_view(url="/", permanent=False)),
    path("accounts/logout/", tender_views.logout_view, name="logout"),
    path("", include("tenders.urls")),
]
