from django.urls import path

from .views import AdminDashboardView, OrganizerDashboardView

app_name = "events"

urlpatterns = [
    path("organizer/dashboard/", OrganizerDashboardView.as_view(), name="organizer_dashboard"),
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
]
