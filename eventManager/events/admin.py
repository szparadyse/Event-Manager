from django.contrib import admin

from .models import Event, EventCategory, EventRegistration, EventReview


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


class EventRegistrationInline(admin.TabularInline):
    model = EventRegistration
    extra = 0


class EventReviewInline(admin.TabularInline):
    model = EventReview
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "organizer", "category", "start_at", "status")
    list_filter = ("status", "category")
    search_fields = ("title", "organizer__username")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EventRegistrationInline, EventReviewInline]


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ("event", "attendee", "checked_in", "registered_at")
    list_filter = ("checked_in",)
    search_fields = ("event__title", "attendee__username")


@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    list_display = ("event", "author", "rating", "created_at")
    list_filter = ("rating",)
    search_fields = ("event__title", "comment")
