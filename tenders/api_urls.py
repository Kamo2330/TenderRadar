from django.urls import path

from . import api_views

urlpatterns = [
    path("auth/login/", api_views.LoginAPIView.as_view(), name="api_login"),
    path("auth/logout/", api_views.LogoutAPIView.as_view(), name="api_logout"),
    path("auth/me/", api_views.MeAPIView.as_view(), name="api_me"),
    path("tenders/", api_views.TenderListAPIView.as_view(), name="api_tender_list"),
    path("tenders/meta/", api_views.TenderMetaAPIView.as_view(), name="api_tender_meta"),
    path(
        "tenders/<int:pk>/",
        api_views.TenderDetailAPIView.as_view(),
        name="api_tender_detail",
    ),
    path(
        "preferences/",
        api_views.AlertPreferenceAPIView.as_view(),
        name="api_preferences",
    ),
]
