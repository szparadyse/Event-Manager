from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone


class EventCategory(models.Model):
    """Simple lookup table for categorising events."""

    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - debug aid only
        return self.name


class Event(models.Model):
    """Event owned by an organiser."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Brouillon"
        PUBLISHED = "published", "Publié"
        CLOSED = "closed", "Clôturé"
        ARCHIVED = "archived", "Archivé"

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events",
    )
    category = models.ForeignKey(
        EventCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_at"]
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["start_at"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - debug aid only
        return self.title

    @property
    def is_active(self) -> bool:
        return self.status in {self.Status.PUBLISHED, self.Status.CLOSED}

    def has_started(self) -> bool:
        return timezone.now() >= self.start_at


class EventRegistration(models.Model):
    """Registration of an attendee to an event."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="registrations",
    )
    attendee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="event_registrations",
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)

    class Meta:
        unique_together = ("event", "attendee")
        ordering = ["-registered_at"]

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.attendee} -> {self.event}"


class EventReview(models.Model):
    """Feedback left by attendees."""

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="event_reviews",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["rating"])]

    def __str__(self) -> str:  # pragma: no cover
        return f"Avis {self.rating}/5 pour {self.event}"

    def clean(self) -> None:
        if self.rating < 1 or self.rating > 5:
            raise models.ValidationError("La note doit être comprise entre 1 et 5.")
