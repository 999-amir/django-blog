from home.models import FastAccessModel


def fast_access_links(request):
    fast_access_data = FastAccessModel.objects.all()
    return {
        "fast_access_data": fast_access_data,
    }
