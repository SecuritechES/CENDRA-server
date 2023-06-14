from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from CENDRA.utils import DynamicFieldsSerializer
from apps.entity.models import Entity, Directorate, DirectoratePosition
from apps.affiliate.models import Affiliate
from apps.affiliate.serializers import AffiliateSerializer


class DirectoratePositionSerializer(DynamicFieldsSerializer):
    class Meta:
        model = DirectoratePosition
        exclude = ['entity']

class EntitySerializer(DynamicFieldsSerializer):

    class Meta:
        model = Entity
        exclude = ['is_same_address']
        depth = 1

class DirectorateSerializer(DynamicFieldsSerializer):
    class Meta:
        model = Directorate
        exclude = ['entity']
