from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import NewsItem
from .serializers import NewsSerializer

class News(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="News item ID to retrieve", type=openapi.TYPE_INTEGER, required=False)
        ],
        responses={
            200: openapi.Response("Successful request.", NewsSerializer),
            400: openapi.Response("Bad request."),
        }
    )
    def get(self, request, *args, **kwargs):
        """
        Retrieves the News. 

        If query param 'id' is provided, returns only one object.
        """
        news_id = self.request.query_params.get('id')
        if news_id:
            try:
                int(news_id)
                news = get_object_or_404(NewsItem, pk=news_id, entity=request.user.entity)
                serializer = NewsSerializer(news, many=False)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            news = NewsItem.objects.filter(entity=request.user.entity.id)
            serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=NewsSerializer)
    def post(self, request, *args, **kwargs):
        """
        Create a news item.

        Returns the created news item object.
        """
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(entity=request.user.entity, author=request.user.affiliate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="News item ID to update", type=openapi.TYPE_INTEGER, required=True)
        ],
        request_body=NewsSerializer
    )
    def patch(self, request, *args, **kwargs):
        """
        Update a news item.

        The news item ID must be provided over the query param 'id'.
        If successful, returns the updated news item as a JSON object.
        """
        news_id = self.request.query_params.get('id')
        if news_id:
            try:
                int(news_id)
                item = get_object_or_404(NewsItem, pk=news_id, entity=request.user.entity)
                serializer = NewsSerializer(instance=item, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="News item ID to delete", type=openapi.TYPE_INTEGER, required=True)
        ]
    )
    def delete(self, request, *args, **kwargs):
        """
        Delete a news item.

        The news item ID must be provided over the query param 'id'.
        If successful, returns the updated news item as a JSON object.
        """
        news_id = self.request.query_params.get('id')
        if news_id:
            try:
                int(news_id)
                item = get_object_or_404(NewsItem, pk=news_id, entity=request.user.entity)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)