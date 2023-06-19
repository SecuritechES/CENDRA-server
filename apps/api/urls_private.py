import os
from django.urls import path, re_path
from rest_framework import permissions, routers
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from CENDRA.api_views import Dashboard
from apps.affiliate.api_views import Affiliates, PaymentChoices, UpdatePhoto, ExportAffiliates, AffiliateViewSet, PaymentChoicesViewSet
from apps.entity.api_views import EntityPrivate, EntityJoin, DirectoratePositions, Directorates, CreateYearlyCensus, EntityViewSet, DirectoratePositionsViewSet
from apps.news.api_views import News
from apps.treasury.api_views import BankAccounts, Transactions
from apps.user.api_views import UserRegisterAffiliate, UserPrivate


class PrivateSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super(PrivateSchemaGenerator, self).get_schema(request, public)
        schema.basePath = os.path.join(schema.basePath, 'api/private/')
        schema.schemes = ["http", "https"]
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

router = routers.DefaultRouter()
router.register(r'v2/affiliates', AffiliateViewSet)
router.register(r'v2/affiliates/payments', PaymentChoicesViewSet)
router.register(r'v2/entities', EntityViewSet)
router.register(r'v2/entity/positions', DirectoratePositionsViewSet)

urlpatterns = [
    path('dashboard', Dashboard.as_view()),
    path('user', UserPrivate.as_view()),
    path('user/affiliate', UserRegisterAffiliate.as_view()),
    path('user/photo', UpdatePhoto.as_view()),
    path('entity', EntityPrivate.as_view()),
    path('entity/join', EntityJoin.as_view()),
    path('entity/positions', DirectoratePositions.as_view()),
    path('entity/directorate', Directorates.as_view()),
    path('entity/census', CreateYearlyCensus.as_view()),
    path('affiliates', Affiliates.as_view()),
    path('affiliates/paymentchoice', PaymentChoices.as_view()),
    path('affiliates/export', ExportAffiliates.as_view()),
    path('treasury', BankAccounts.as_view()),
    path('treasury/transactions', Transactions.as_view()),
    path('news', News.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view_private.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view_private.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view_private.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += router.urls