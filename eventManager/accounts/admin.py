from django.contrib import admin
from .models import Events, EventReviews, Answers, Categories

admin.site.register(Events)
admin.site.register(EventReviews)
admin.site.register(Answers)
admin.site.register(Categories)