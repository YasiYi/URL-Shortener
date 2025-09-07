from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect
from ..models import *
from ..utils.user_agent import detect_browser, detect_device_type
from rest_framework import generics, permissions
from ..serializers import *

class CreateShortUrlView(generics.CreateAPIView):
    serializer_class = URLCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return URL.objects.filter(created_by=self.request.user)

class RedirectView(APIView):
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        return x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

    def get(self, request, short_url):
        url_obj = get_object_or_404(URL, short_url=short_url, enabled=True)

        user_agent = request.headers.get("User-Agent", "")
        ip = self.get_client_ip(request)

        Visit.objects.create(
            url=url_obj,
            ip_address=ip,
            user_agent=user_agent,
            device_type=detect_device_type(user_agent),
            browser=detect_browser(user_agent),
        )

        return redirect(url_obj.original_url)