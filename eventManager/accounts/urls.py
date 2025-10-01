from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView

app_name = 'accounts'

urlpatterns = [
  path('login/', LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
  path('signup/', SignUpView.as_view(), name='signup'),
]