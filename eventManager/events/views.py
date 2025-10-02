from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Avg, Count, Q, Value
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

from .models import Event, EventRegistration, EventReview

User = get_user_model()


class StaffRequiredMixin(UserPassesTestMixin):
    """Ensure the current user has staff capabilities."""

    def test_func(self) -> bool:
        return self.request.user.is_staff


class OrganizerDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "events/organizer_dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        events_qs = (
            Event.objects.filter(organizer=self.request.user)
            .select_related("category")
            .annotate(
                registrations_count=Count("registrations", distinct=True),
                checked_in_count=Count(
                    "registrations",
                    filter=Q(registrations__checked_in=True),
                    distinct=True,
                ),
                reviews_count=Count("reviews", distinct=True),
                average_rating=Avg("reviews__rating"),
            )
            .order_by("-start_at")
        )

        registration_totals = EventRegistration.objects.filter(
            event__organizer=self.request.user
        ).aggregate(
            total_registrations=Count("id", distinct=True),
            total_checked_in=Count("id", filter=Q(checked_in=True), distinct=True),
        )

        reviews_totals = EventReview.objects.filter(event__organizer=self.request.user).aggregate(
            total_reviews=Count("id", distinct=True),
            average_rating=Avg("rating"),
        )

        total_registrations = registration_totals["total_registrations"] or 0
        total_checked_in = registration_totals["total_checked_in"] or 0
        participation_rate = (
            (total_checked_in / total_registrations) * 100 if total_registrations else 0.0
        )

        context.update(
            dashboard_user=self.request.user,
            events=events_qs,
            total_registrations=total_registrations,
            participation_rate=round(participation_rate, 2),
            total_reviews=reviews_totals["total_reviews"] or 0,
            average_rating=reviews_totals["average_rating"],
        )
        return context


class AdminDashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "events/admin_dashboard.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        totals = {
            "users": User.objects.filter(is_active=True).count(),
            "events": Event.objects.count(),
            "registrations": EventRegistration.objects.count(),
            "reviews": EventReview.objects.count(),
        }

        category_distribution = (
            Event.objects.annotate(
                category_name=Coalesce("category__name", Value("Sans catégorie"))
            )
            .values("category_name")
            .annotate(total=Count("id"))
            .order_by("-total")
        )

        top_events = (
            Event.objects.annotate(
                average_rating=Avg("reviews__rating"),
                reviews_count=Count("reviews", distinct=True),
                registrations_count=Count("registrations", distinct=True),
            )
            .filter(reviews_count__gt=0)
            .select_related("category", "organizer")
            .order_by("-average_rating", "-reviews_count")[:10]
        )

        context.update(
            totals=totals,
            category_distribution=category_distribution,
            top_events=top_events,
        )
        return context
