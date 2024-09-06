from rest_framework.views import APIView
from rest_framework.response import Response
from home.views import track_previous_days
from accounts.models import TrackingUserModel
from blog.models import BlogModel
from message.models import MessageModel
from datetime import datetime, timedelta


class HomeAPIView(APIView):
    def get(self, request):
        systems = []
        if request.user.is_authenticated:
            user_tracks = TrackingUserModel.objects.filter(
                user=request.user,
                created__gte=datetime.now() - timedelta(days=10),
            )
            for user_track in user_tracks:
                if not (user_track.system in systems):
                    systems.append(user_track.system)
        else:
            systems = None
        context = {
            "track_users": track_previous_days(
                TrackingUserModel.objects.all()
            ),
            "track_blog": track_previous_days(BlogModel.objects.all()),
            "track_messages": track_previous_days(MessageModel.objects.all()),
            "systems": systems,
        }
        return Response(context)
