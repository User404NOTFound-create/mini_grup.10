from django.urls import path
from core.views.auth_views import RegisterView

urlpatterns = [
      path('register/', RegisterView.as_view())
]