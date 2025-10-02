from __future__ import annotations

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Event, EventCategory, EventRegistration, EventReview

User = get_user_model()


class OrganizerDashboardTests(TestCase):
    def setUp(self) -> None:
        self.organizer = User.objects.create_user(
            username="organizer",
            password="secret123",
            email="organizer@example.com",
        )
        self.category = EventCategory.objects.create(name="Tech")
        start = timezone.now() + timedelta(days=2)
        end = start + timedelta(hours=3)
        self.event = Event.objects.create(
            organizer=self.organizer,
            category=self.category,
            title="Conférence Django",
            slug="conference-django",
            start_at=start,
            end_at=end,
            status=Event.Status.PUBLISHED,
        )
        attendee = User.objects.create_user(
            username="attendee",
            password="secret123",
            email="attendee@example.com",
        )
        EventRegistration.objects.create(
            event=self.event,
            attendee=attendee,
            checked_in=True,
        )
        EventReview.objects.create(
            event=self.event,
            author=attendee,
            rating=5,
            comment="Super événement",
        )

    def test_dashboard_context_contains_stats(self) -> None:
        self.client.login(username="organizer", password="secret123")
        response = self.client.get(reverse("events:organizer_dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_registrations"], 1)
        self.assertEqual(response.context["total_reviews"], 1)
        self.assertAlmostEqual(response.context["participation_rate"], 100.0)
        events = list(response.context["events"])
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].registrations_count, 1)
        self.assertEqual(events[0].reviews_count, 1)


class AdminDashboardTests(TestCase):
    def setUp(self) -> None:
        self.staff = User.objects.create_user(
            username="admin",
            password="secret123",
            email="admin@example.com",
            is_staff=True,
        )
        organizer = User.objects.create_user(
            username="another",
            password="secret123",
            email="another@example.com",
        )
        category = EventCategory.objects.create(name="Business")
        start = timezone.now() + timedelta(days=5)
        event = Event.objects.create(
            organizer=organizer,
            category=category,
            title="Salon Pro",
            slug="salon-pro",
            start_at=start,
            end_at=start + timedelta(hours=4),
            status=Event.Status.PUBLISHED,
        )
        EventRegistration.objects.create(
            event=event,
            attendee=self.staff,
            checked_in=False,
        )
        EventReview.objects.create(
            event=event,
            author=self.staff,
            rating=4,
        )

    def test_admin_dashboard_requires_staff(self) -> None:
        non_staff = User.objects.create_user(
            username="simple",
            password="secret123",
            email="simple@example.com",
        )
        self.client.login(username="simple", password="secret123")
        response = self.client.get(reverse("events:admin_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_admin_dashboard_stats(self) -> None:
        self.client.login(username="admin", password="secret123")
        response = self.client.get(reverse("events:admin_dashboard"))
        self.assertEqual(response.status_code, 200)
        totals = response.context["totals"]
        self.assertGreaterEqual(totals["users"], 1)
        self.assertEqual(totals["events"], 1)
        self.assertEqual(totals["registrations"], 1)
        self.assertEqual(totals["reviews"], 1)
        self.assertTrue(response.context["category_distribution"])
        self.assertTrue(response.context["top_events"])
