from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include(('djoser.urls.jwt'))),
]

schema_view = get_schema_view(
    openapi.Info(
        title='Shop API',
        default_version='v1',
        description='Документация для проекта shop для приложения Django-shop',
        contact=openapi.Contact(email='admin@django_shop.ru'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns += [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
            name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]
