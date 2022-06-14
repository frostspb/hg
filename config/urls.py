from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from rest_framework_simplejwt.views import (

    TokenRefreshView,
)

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from ajax_select import urls as ajax_select_urls

from hourglass.campaigns.api.views import CFilesUpload, DealDeskView
from .auth import CurrentUserView, ExtendedTokenObtainPairView

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    url(r'^ajax_select/', include(ajax_select_urls)),
    path('admin/', admin.site.urls),
    path("api/", include("config.router")),
    path('api/auth/', include(
        'rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token/obtain/', ExtendedTokenObtainPairView.as_view(), ),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/auth/user/', CurrentUserView.as_view()),
    path('api/cr_files_upload/', CFilesUpload.as_view()),
    path('api/deal_desk/', DealDeskView.as_view()),

    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^chaining/', include('smart_selects.urls')),
]

admin.autodiscover()
admin.site.enable_nav_sidebar = False

admin.site.site_header = 'Hourglass Admin Panel'
admin.site.site_title = 'Hourglass Admin Panel'
