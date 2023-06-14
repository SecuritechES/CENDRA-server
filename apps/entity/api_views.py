from io import BytesIO
import xlsxwriter
import datetime
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from apps.affiliate.models import Affiliate
from .models import Entity, DirectoratePosition, Directorate, YearlyCensus, YearlyCensusEntry
from .serializers import EntitySerializer, DirectoratePositionSerializer, DirectorateSerializer

class EntityPublic(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="Entity ID to retrieve", type=openapi.TYPE_INTEGER, required=False)
        ],
        responses={
            200: openapi.Response("Successful request.", EntitySerializer(fields=('id', 'name', 'logo'))),
            400: openapi.Response("Bad request."),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Returns an array of entities with basic info only. 

        If query param 'id' is provided, returns only one object.
        """
        entity_id = self.request.query_params.get('id')
        if entity_id:
            try:
                entities = get_object_or_404(Entity, pk=entity_id)
                serializer = EntitySerializer(entities, many=False, fields=('id', 'name', 'logo'))
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            entities = Entity.objects.all()
            serializer = EntitySerializer(entities, many=True, fields=('id', 'name', 'logo'))
        return Response(serializer.data)
    
class EntityPrivate(APIView):
    @swagger_auto_schema(
            responses={
                200: openapi.Response("Successful request.", EntitySerializer),
                400: openapi.Response("Bad request."),
            }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieve the current user entity data.

        Returns the full entity object.
        """
        entity = get_object_or_404(Entity, pk=request.user.entity.id)
        serializer = EntitySerializer(entity)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EntitySerializer)
    def post(self, request, *args, **kwargs):
        """
        Create a new entity.
        
        Returns the created entity object
        """
        serializer = EntitySerializer(data=request.data, fields=('name', 'social_address', 'postal_code', 'city', 'province'))
        if serializer.is_valid():
            entity = serializer.save()
            request.user.entity = entity
            request.user.is_entity_admin = True
            request.user.onboarding = 1
            request.user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=EntitySerializer)
    def patch(self, request, *args, **kwargs):
        """
        Update the current user entity data.
        
        Returns the updated entity object
        """
        entity = get_object_or_404(Entity, pk=request.user.entity.id)
        serializer = EntitySerializer(instance=entity, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EntityJoin(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Entity ID'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Entity join password')
            },
            required=['id', 'password']
        ),
        responses={
            201: openapi.Response("Successful request.", EntitySerializer),
            401: openapi.Response("Incorrect password"),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Joins the current user to a existing entity.
        
        Returns the joined entity object
        """
        try:
            entity_id = request.data["id"]
            password = request.data["password"]
            entity = Entity.objects.get(pk=entity_id, join_password=password)
            request.user.entity = entity
            request.user.onboarding = 1
            request.user.save()
            serializer = EntitySerializer(entity)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
class DirectoratePositions(APIView):
    @swagger_auto_schema(
            responses={
                200: openapi.Response("Successful request.", DirectoratePositionSerializer),
                400: openapi.Response("Bad request."),
            }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieves the existing positions on the user entity.

        Returns an array of DirectoratePositions.
        """
        positions = DirectoratePosition.objects.filter(entity=request.user.entity.id)
        serializer = DirectoratePositionSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DirectoratePositionSerializer)
    def post(self, request, *args, **kwargs):
        """
        Create a new position on the user entity.

        Returns the created position object.
        """
        serializer = DirectoratePositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(entity=request.user.entity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('id', openapi.IN_QUERY, description="Position ID to update", type=openapi.TYPE_INTEGER, required=True)
            ],
            request_body=DirectoratePositionSerializer
    )
    def patch(self, request, *args, **kwargs):
        """
        Update a position name.

        The position ID must be provided over the query param 'id'.
        If successful, returns the updated position as a JSON object.
        """
        position_id = self.request.query_params.get('id')
        if position_id:
            try:
                int(position_id)
                item = get_object_or_404(DirectoratePosition, pk=position_id, entity=request.user.entity)
                serializer = DirectoratePositionSerializer(instance=item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Deletes a position name.

        The position ID must be provided over the query param 'id'.
        If successful, returns the HTTP code 204
        """
        position_id = self.request.query_params.get('id')
        if position_id:
            try:
                int(position_id)
                item = get_object_or_404(DirectoratePosition, pk=position_id, entity=request.user.entity)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class Directorates(APIView):
    @swagger_auto_schema(
            responses={
                200: openapi.Response("Successful request.", DirectorateSerializer),
                400: openapi.Response("Bad request."),
            }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieves the entity directorate.

        Returns an array of Directorates.
        """
        positions = Directorate.objects.filter(entity=request.user.entity.id)
        serializer = DirectorateSerializer(positions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DirectorateSerializer)
    def post(self, request, *args, **kwargs):
        """
        Create a new directorate.

        Returns the created directorate object.
        """
        user = get_object_or_404(Affiliate, pk=request.data["user"], entity=request.user.entity.id)
        position = get_object_or_404(DirectoratePosition, pk=request.data["position"], entity=request.user.entity.id)
        if Directorate.objects.filter(user=user).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = DirectorateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(entity=request.user.entity, user=user, position=position)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            request_body=DirectorateSerializer,
            manual_parameters=[
                openapi.Parameter('id', openapi.IN_QUERY, description="Position ID to update", type=openapi.TYPE_INTEGER, required=True)
            ]
    )
    def patch(self, request, *args, **kwargs):
        """
        Update a directorate.

        The directorate ID must be provided over the query param 'id'.
        If successful, returns the updated directorate as a JSON object.
        """
        directorate_id = self.request.query_params.get('id')
        if directorate_id:
            try:
                int(directorate_id)
                user = get_object_or_404(Affiliate, pk=request.data["user"], entity=request.user.entity.id)
                position = get_object_or_404(DirectoratePosition, pk=request.data["position"], entity=request.user.entity.id)
                item = get_object_or_404(Directorate, pk=directorate_id, entity=request.user.entity)
                serializer = DirectorateSerializer(instance=item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save(entity=request.user.entity, user=user, position=position)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        """
        Deletes a directorate.

        The position ID must be provided over the query param 'id'.
        If successful, returns the HTTP code 204
        """
        directorate_id = self.request.query_params.get('id')
        if directorate_id:
            try:
                int(directorate_id)
                item = get_object_or_404(DirectoratePosition, pk=directorate_id, entity=request.user.entity)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class CreateYearlyCensus(APIView):
    @swagger_auto_schema(responses={
                200: openapi.Response("Successful request."),
                401: openapi.Response("User is not entity admin."),
            })
    def post(self, request, *args, **kwargs):
        """ 
        Generates an excel report of affiliates of the current user entity.

        """
        if(request.user.is_entity_admin):
            YearlyCensus.objects.filter(entity=request.user.entity, year=datetime.datetime.now().year).delete()
            affiliates = Affiliate.objects.filter(entity=request.user.entity.id, active=True)
            census = YearlyCensus.objects.create(entity=request.user.entity, year=datetime.datetime.now().year)
            census.save()
            for affiliate in affiliates:
                entry = YearlyCensusEntry.objects.create(
                    affiliate=affiliate,
                    jcf_number=affiliate.jcf_number,
                    census_number=affiliate.census_number,
                    commission="MAY",
                    surnames=affiliate.surnames,
                    name=affiliate.name,
                    address=affiliate.address,
                    city=affiliate.city,
                    postal_code=affiliate.postal_code,
                    phone=affiliate.phone,
                    birthday=affiliate.birthday,
                    gender=affiliate.gender,
                    document_id=affiliate.document_id,
                    position=affiliate.position,
                    reward=""
                )
                entry.save()
                census.entries.add(entry)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)