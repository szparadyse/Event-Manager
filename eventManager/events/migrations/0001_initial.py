from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=220, unique=True)),
                ('description', models.TextField(blank=True)),
                ('location', models.CharField(blank=True, max_length=255)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('capacity', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('draft', 'Brouillon'), ('published', 'Publié'), ('closed', 'Clôturé'), ('archived', 'Archivé')], default='draft', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='events.eventcategory')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organized_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-start_at'],
            },
        ),
        migrations.CreateModel(
            name='EventReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_reviews', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='events.event')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('checked_in', models.BooleanField(default=False)),
                ('attendee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_registrations', to=settings.AUTH_USER_MODEL)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='events.event')),
            ],
            options={
                'ordering': ['-registered_at'],
                'unique_together': {('event', 'attendee')},
            },
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['status'], name='events_event_status_idx'),
        ),
        migrations.AddIndex(
            model_name='event',
            index=models.Index(fields=['start_at'], name='events_event_start_idx'),
        ),
        migrations.AddIndex(
            model_name='eventreview',
            index=models.Index(fields=['rating'], name='events_event_rating_idx'),
        ),
    ]
