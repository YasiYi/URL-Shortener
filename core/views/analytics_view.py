from django.db.models import Count
from datetime import datetime, time, timedelta
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Visit, URL


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, short_url):
        url_obj = get_object_or_404(URL, short_url=short_url)

        range_param = request.query_params.get("range", "7d")
        now_time = now()

        time_ranges = {
            "today": datetime.combine(now_time.date(), time.min),
            "24h": now_time - timedelta(hours=24),
            "7d": now_time - timedelta(days=7),
            "30d": now_time - timedelta(days=30),
        }

        start_time = time_ranges.get(range_param, time_ranges["7d"])
        qs = Visit.objects.filter(url=url_obj, timestamp__gte=start_time)

        by_device_qs = qs.values("device_type").annotate(count=Count("id"))
        by_device = {item['device_type']: item['count'] for item in by_device_qs}

        by_browser_qs = qs.values("browser").annotate(count=Count("id"))
        by_browser = {item['browser']: item['count'] for item in by_browser_qs}

        return Response({
            "total_views": qs.count(),
            "unique_users": qs.values("ip_address").distinct().count(),
            "by_device": by_device,
            "by_browser": by_browser,
        })