from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta
from accounts.models import TrackingUserModel
from blog.models import BlogModel
from message.models import MessageModel


def track_previous_days(objects):
    data = {
        'count': [],
        'date': []
    }
    for i in range(31, -1, -1):  # count reverse from 10 days ago to today
        date = datetime.now() - timedelta(days=i)
        objs = objects.filter(created=date)
        data['count'].append(objs.count())
        data['date'].append(int(date.strftime("%d")))
    return data


class HomeView(View):
    def get(self, request):
        systems = []
        if request.user.is_authenticated:
            user_tracks = TrackingUserModel.objects.filter(user=request.user, created__gte=datetime.now()-timedelta(days=10))
            for user_track in user_tracks:
                if not user_track.system in systems:
                    systems.append(user_track.system)
        else:
            systems = None
        context = {
            'track_users': track_previous_days(TrackingUserModel.objects.all()),
            'track_blog': track_previous_days(BlogModel.objects.all()),
            'track_messages': track_previous_days(MessageModel.objects.all()),
            'systems': systems
        }
        return render(request, 'home/HOME.html', context)
