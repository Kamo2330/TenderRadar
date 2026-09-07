from django.urls import path

from . import views

app_name = "tenders"

urlpatterns = [
    path("health/", views.health_check, name="health"),
    path("", views.dashboard, name="dashboard"),
    path("preferences/", views.preferences, name="preferences"),
    # Client portal
    path("client/tenders/", views.client_tenders, name="client_tenders"),
    path("client/tenders/<int:tender_id>/apply/", views.client_apply, name="client_apply"),
    # Staff capture & client management
    path("staff/clients/", views.staff_client_list, name="staff_client_list"),
    path("staff/clients/new/", views.staff_client_create, name="staff_client_create"),
    # Staff managed coverage dashboard
    path("staff/managed/", views.staff_managed_overview, name="staff_managed_overview"),
    path(
        "staff/managed/<int:client_id>/",
        views.staff_client_coverage_detail,
        name="staff_client_coverage_detail",
    ),
    # Staff applications queue
    path("staff/applications/", views.staff_applications_queue, name="staff_applications_queue"),
]


