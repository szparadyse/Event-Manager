"""
URL configuration for eventManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from accounts.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('', include('events.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
]
