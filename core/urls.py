from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .Views.users_view import RegisterView
from .Views.shortner_view import RedirectView, CreateShortUrlView

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token_refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path("shorten/", CreateShortUrlView.as_view(), name="create_short_url"),
    path("r/<str:short_url>/", RedirectView.as_view(), name="redirect"),
    path('analytics/<str:short_url>/', AnalyticsView.as_view(), name='analytics'),
]
