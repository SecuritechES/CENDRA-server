import os
from django.urls import path, re_path
from rest_framework import permissions
from rest_framework.authtoken import views
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from apps.entity.api_views import EntityPublic
from apps.user.api_views import UserRegister

class PublicSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=True):
        schema = super(PublicSchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(schema.basePath, 'api/public/')
        schema.schemes = ["http", "https"]
        return schema

openapi_info = openapi.Info(
    title='CENDRA API',
    default_version='v1',
    description='Public API for CENDRA',
    contact=openapi.Contact(email='afuentes.xtv@gmail.com')
    )

schema_view_public = get_schema_view(
    openapi_info,
    permission_classes=[permissions.AllowAny],
    urlconf="apps.api.urls_public",
    generator_class=PublicSchemaGenerator
)

urlpatterns = [
    path('register', UserRegister.as_view()),
    path('entities', EntityPublic.as_view()),
    path('token', views.obtain_auth_token),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_public.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_public.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_public.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]