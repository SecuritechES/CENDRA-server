from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.entity.models import Entity
from apps.affiliate.serializers import AffiliateSerializer
from apps.user.serializers import UserRegisterSerializer, UserUpdateSerializer, UserSerializer
from rest_framework.authtoken.models import Token

class UserRegister(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handles the POST request for register an user.
        
        :returns: json response with auth token of the created user
        """
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterAffiliate(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        
        if data["document_type"] == "DNI":
            data["document_type"] = 1
        elif data["document_type"] == "NIE":
            data["document_type"] = 2
        if data["document_type"] == "Pasaporte":
            data["document_type"] = 3

        serializer = AffiliateSerializer(data=data)
        if serializer.is_valid():
            affiliate = serializer.save(entity=request.user.entity)
            request.user.affiliate = affiliate
            request.user.onboarding = 99
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserPrivate(APIView):
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Handles the PATCH request for update an user entity.
        
        :returns: json response with entity id
        """
        user = request.user
        if request.data["entity"]:
            entity = get_object_or_404(Entity, pk=request.data["entity"])
            serializer = UserUpdateSerializer(instance=user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'entity':entity.name, 'id':entity.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

