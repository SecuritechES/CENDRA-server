from rest_framework import serializers
from CENDRA.utils import DynamicFieldsSerializer
from .models import NewsItem


class NewsSerializer(DynamicFieldsSerializer):
    authorstr = serializers.CharField()

    class Meta:
        model = NewsItem
        exclude = ['entity']

    def get_authorstr(self, instance):
        return self.authorstr