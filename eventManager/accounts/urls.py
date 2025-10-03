from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView, event_list, event_details, add_event, add_review, add_answer, ProfileView

app_name = 'accounts'

urlpatterns = [
  path('login/', LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
  path('signup/', SignUpView.as_view(), name='signup'),
  path('events/', event_list, name='event_list'),
  path('events/add/', add_event, name='add_event'),
  path('events/<int:event_id>/', event_details, name='event_details'),
  path('events/<int:event_id>/add_review/', add_review, name='add_review'),
  path('reviews/<int:review_id>/add_answer/', add_answer, name='add_answer'),
  path('profile/', ProfileView.as_view(), name='profile'),
]