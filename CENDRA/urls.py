"""CENDRA URL Configuration"""
import os
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework.authtoken import views
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator

class PrivateSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(PrivateSchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(schema.basePath, 'api/private/')
        schema.schemes = ["https"]
        return schema

schema_view_private = get_schema_view(
    openapi.Info(
    title='CENDRA API',
    default_version='v1',
    description='Private API for CENDRA',
    contact=openapi.Contact(email='afuentes.xtv@gmail.com')
    ),
    permission_classes=[permissions.IsAuthenticated],
    urlconf="apps.api.urls_private",
    generator_class=PrivateSchemaGenerator
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/public/', include('apps.api.urls_public')),
    path('api/private/', include('apps.api.urls_private')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
