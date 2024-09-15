from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.views.generic import TemplateView

# ====================================================================| APPS
# apps & admin path
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls", namespace="home")),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("message/", include("message.urls", namespace="message")),
    path(
        "private-data/",
        include("private_data.urls", namespace="private-data"),
    ),
]

# ====================================================================| FILES, COMING-SOON, DEBUG, STATUS
# media & static path
if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

# coming soon
if settings.COMINGSOON:
    urlpatterns.insert(
        0, re_path(r"^", TemplateView.as_view(template_name="comingsoon.html"))
    )

# debug
if settings.SHOW_DEBUGGER_TOOLBAR:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]


handler400 = "core.error_views.error_400"  # bad_request
handler403 = "core.error_views.error_403"  # permission_denied
handler404 = "core.error_views.error_404"  # page_not_found
handler500 = "core.error_views.error_500"  # server_error

# ====================================================================| API DOC, VIEW
# schema view
schema_view = get_schema_view(
    openapi.Info(
        title="todo-app",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="MIT license"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

# swagger
if settings.SHOW_SWAGGER:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls",
                                  namespace="rest_framework")),
        path(
            "swagger/api.json",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]