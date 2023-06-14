from rest_framework import serializers
from CENDRA.utils import DynamicFieldsSerializer
from apps.affiliate.models import Affiliate, PaymentChoice

class PaymentChoiceSerializer(DynamicFieldsSerializer):
    class Meta:
        model = PaymentChoice
        exclude = ['affiliate', 'id']

class AffiliateSerializer(DynamicFieldsSerializer):
    photo = serializers.ImageField(required=False)
    payment_choice = PaymentChoiceSerializer(required=False)
    position = serializers.CharField(required=False)

    def get_position(self, instance):
        return self.position
    
    class Meta:
        model = Affiliate
        exclude = ['entity']

class PaymentChoiceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentChoice
        fields = ['affiliate', 'payment_type', 'account_holder', 'account_iban']
