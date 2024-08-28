from .models import TrackingUserModel
from datetime import datetime


class TrackingUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        system = request.META['HTTP_USER_AGENT']

        tracks = TrackingUserModel.objects.filter(ip=ip, system=system, created=datetime.now())
        if request.user.is_authenticated and not tracks.filter(user=request.user).exists():
            TrackingUserModel.objects.create(user=request.user, ip=ip, system=system)
        elif not tracks.exists():
            TrackingUserModel.objects.create(ip=ip, system=system)

        response = self.get_response(request)
        return response
