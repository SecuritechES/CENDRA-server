from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import CendraUser
from apps.entity.models import Entity
from apps.affiliate.serializers import AffiliateSerializer


class UserSerializer(serializers.ModelSerializer):
    entity = serializers.StringRelatedField(read_only=True)
    affiliate = AffiliateSerializer(read_only=True)
    class Meta:
        model = CendraUser
        fields = [
            'email',
            'entity',
            'is_entity_admin',
            'affiliate',
            'onboarding'
        ]

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CendraUser
        fields = ['email', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CendraUser.objects.create_user(validated_data['email'], validated_data['email'], validated_data['password'])
        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    entity = serializers.PrimaryKeyRelatedField(queryset=Entity.objects.all(), many=False)
    join_password = serializers.CharField(required=True)

    class Meta:
        model = CendraUser
        fields = ['entity', 'join_password']

    def validate(self, data):
        entity = Entity.objects.get(pk=data["entity"].id)
        if entity.join_password != data["join_password"]:
            raise serializers.ValidationError({"join_password": "Incorrect password"})
        return data

# HASTA AQUÍ TODO NUEVO
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CendraUser
        fields = [
            "email", "password"
        ]
        extra_kwargs = {"password": {"write_only": True}}
    
    def create(self, validated_data):
        user = CendraUser.objects.create_user(validated_data['email'], validated_data['email'], validated_data['password'])
        return user

class UserToEntitySerializer(serializers.ModelSerializer):
    entity = serializers.PrimaryKeyRelatedField(queryset=Entity.objects.all(), many=False)
    join_password = serializers.CharField(required=True)
    class Meta:
        model = CendraUser
        fields = [
            "entity", "join_password"
        ]
        extra_kwargs = {"join_password": {"write_only": True, "required": True}}

    def validate(self, data):
        entity = Entity.objects.get(pk=data["entity"].id)
        if entity.join_password != data["join_password"]:
            raise serializers.ValidationError({"join_password": "join_password error"})