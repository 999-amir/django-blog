from accounts.models import TrackingUserModel
from datetime import timedelta, datetime


def track_users_seen(request):
    data = {"count": [], "date": []}
    tracks = TrackingUserModel.objects.all()
    for i in range(10, -1, -1):  # count reverse from 10 days ago to today
        date = datetime.now() - timedelta(days=i)
        track = tracks.filter(created=date)
        data["count"].append(track.count())
        data["date"].append(int(date.strftime("%d")))
    return {
        "track_users_seen": data,
    }
