from io import BytesIO
import datetime
from django.http import HttpResponse
import xlsxwriter
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from CENDRA.permissions import EntityAdminPermission, IsUserOwner
from .models import Affiliate, PaymentChoice
from .serializers import AffiliateSerializer, PaymentChoiceSerializer

class Affiliates(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter(
                    'id', 
                    openapi.IN_QUERY, 
                    description="Affiliate ID to retrieve", 
                    type=openapi.TYPE_INTEGER, required=False
                )
            ],
            responses={
                200: openapi.Response("Successful request.", AffiliateSerializer),
                400: openapi.Response("Bad request."),
            }
    )
    def get(self, request, *args, **kwargs):
        """
        Returns an array of affiliates of the current user entity.

        If query param 'id' is provided, returns only one object.
        """
        affiliate_id = self.request.query_params.get('id')
        if affiliate_id:
            try:
                int(affiliate_id)
                affiliates = get_object_or_404(Affiliate, pk=affiliate_id, entity=request.user.entity)
                serializer = AffiliateSerializer(affiliates, many=False)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            affiliates = Affiliate.objects.filter(entity=request.user.entity.id)
            serializer = AffiliateSerializer(affiliates, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=AffiliateSerializer)
    def post(self, request, *args, **kwargs):
        """
        Creates a new affiliate for the current user entity.

        If successful, returns the created affiliate as a JSON object.
        """
        serializer = AffiliateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(entity=request.user.entity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('id', openapi.IN_QUERY, description="Affiliate ID to update", type=openapi.TYPE_INTEGER, required=True)
            ],
            request_body=AffiliateSerializer
    )
    def patch(self, request, *args, **kwargs):
        """
        Updates the data of an affiliate.

        The affiliate ID must be provided over the query param 'id'.
        If successful, returns the updated affiliate as a JSON object.
        """
        entity_id = self.request.query_params.get('id')
        if entity_id:
            try:
                int(entity_id)
                affiliate = get_object_or_404(Affiliate, pk=entity_id, entity=request.user.entity)
                serializer = AffiliateSerializer(instance=affiliate, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ValueError:
                return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PaymentChoices(APIView):
    @swagger_auto_schema(
            manual_parameters=[
                openapi.Parameter('affiliate', openapi.IN_QUERY, description="Affiliate ID to retrieve", type=openapi.TYPE_INTEGER, required=False)
            ],
            responses={
                200: openapi.Response("Successful request.", AffiliateSerializer),
                400: openapi.Response("Bad request."),
            }
    )
    def get(self, request, *args, **kwargs):
        """
        Get the payment choice of an affiliate.

        The affiliate ID must be provided over the query param 'affiliate'.
        If successful, returns the requested PaymentChoice as a JSON object.
        """
        affiliate_id = self.request.query_params.get('affiliate')
        if affiliate_id:
            try:
                int(affiliate_id)
                affiliate = get_object_or_404(Affiliate, pk=affiliate_id, entity=request.user.entity)
                get_object_or_404(PaymentChoice, affiliate=affiliate.id)
                serializer = AffiliateSerializer(affiliate, fields=('id', 'payment_choice'))
                return Response(serializer.data)
            except ValueError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'affiliate': openapi.Schema(type=openapi.TYPE_INTEGER, description='Affiliate ID'),
                'payment_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Payment Type ID'),
                'account_holder': openapi.Schema(type=openapi.TYPE_STRING, description='Account holder'),
                'account_iban': openapi.Schema(type=openapi.TYPE_STRING, description='Account IBAN')
            },
            required=['id', 'password']
        ),
        responses={
            201: openapi.Response("Successful request.", PaymentChoiceSerializer),
            401: openapi.Response("Incorrect password"),
        }
    )
    def post(self, request, *args, **kwargs):
        """
        Creates a new payment choice for an affiliate.

        If successful, returns the created PaymentChoice as a JSON object.
        """
        serializer = PaymentChoiceSerializer(data=request.data)
        affiliate = get_object_or_404(Affiliate, pk=request.data["affiliate"], entity=request.user.entity.id)
        if serializer.is_valid():
            serializer.save(affiliate=affiliate)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'affiliate': openapi.Schema(type=openapi.TYPE_INTEGER, description='Affiliate ID'),
                'payment_type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Payment Type ID'),
                'account_holder': openapi.Schema(type=openapi.TYPE_STRING, description='Account holder'),
                'account_iban': openapi.Schema(type=openapi.TYPE_STRING, description='Account IBAN')
            },
            required=['id', 'password']
        ),
        responses={
            201: openapi.Response("Successful request.", PaymentChoiceSerializer),
            401: openapi.Response("Incorrect password"),
        }
    )
    def patch(self, request, *args, **kwargs):
        """
        Updates the payment choice for the affiliate provided.
        
        If successful, returns the updated PaymentChoice as a JSON object.
        """
        affiliate = get_object_or_404(Affiliate, pk=request.data["affiliate"], entity=request.user.entity.id)
        payment_choice = get_object_or_404(PaymentChoice, affiliate=affiliate)
        serializer = PaymentChoiceSerializer(instance=payment_choice, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class UpdatePhoto(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema()
    def post(self, request, *args, **kwargs):
        """
        Updates the photo of a given affiliate.
        """
        affiliate_id = self.request.query_params.get('id')
        if affiliate_id:
            affiliate = get_object_or_404(Affiliate, pk=affiliate_id, entity=request.user.entity.id)
        else:
            affiliate = get_object_or_404(Affiliate, pk=request.user.affiliate.id, entity=request.user.entity.id)
        data = {"photo":request.data.get('file')}
        serializer = AffiliateSerializer(instance=affiliate, data=data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ExportAffiliates(APIView):
    @swagger_auto_schema(responses={
                200: openapi.Response("Successful request."),
                401: openapi.Response("User is not entity admin."),
            })
    def get(self, request, *args, **kwargs):
        """ 
        Generates an excel report of affiliates of the current user entity.

        """
        if(request.user.is_entity_admin):
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)
            header = workbook.add_format({'bold': True})
            worksheet = workbook.add_worksheet()
            worksheet.write(0, 0, 'COD.JCF', header)
            worksheet.write(0, 1, 'NUM.CENSO', header)
            worksheet.write(0, 2, 'SU.REF.', header)
            worksheet.write(0, 3, 'INF/MAY', header)
            worksheet.write(0, 4, 'APELLIDOS', header)
            worksheet.write(0, 5, 'NOMBRE', header)
            worksheet.write(0, 6, 'DIRECCION', header)
            worksheet.write(0, 7, 'POBLACION', header)
            worksheet.write(0, 8, 'C.POSTAL', header)
            worksheet.write(0, 9, 'TELEF1', header)
            worksheet.write(0, 10, 'TELEF2', header)
            worksheet.write(0, 11, 'F.NAC.', header)
            worksheet.write(0, 12, 'SEXO', header)
            worksheet.write(0, 13, 'DNI', header)
            worksheet.write(0, 14, 'CARGO', header)
            worksheet.write(0, 15, 'RECOMPENSA', header)
            affiliates = Affiliate.objects.filter(entity=request.user.entity.id, active=True)
            i = 1
            for affiliate in affiliates:
                worksheet.write(i, 0, affiliate.jcf_number)
                worksheet.write(i, 1, affiliate.census_number)
                worksheet.write(i, 2, "")
                # Calculate affiliate years in next march
                current = datetime.datetime.now()
                year = current.year
                if(current.month > 3):
                    year += 1
                if year < 16:
                    worksheet.write(i, 3, "INF")
                else:
                    worksheet.write(i, 3, "MAY")
                worksheet.write(i, 4, affiliate.surnames.upper)
                worksheet.write(i, 5, affiliate.name.upper)
                worksheet.write(i, 6, affiliate.address.upper)
                worksheet.write(i, 7, affiliate.city.upper)
                worksheet.write(i, 8, affiliate.postal_code)
                worksheet.write(i, 9, affiliate.phone)
                worksheet.write(i, 10, "")
                worksheet.write(i, 11, str(affiliate.birthday))
                # Fill the gender according to JCF nomenclature. Male = H; Female = M
                gender = "H"
                if(affiliate.gender == "F"):
                    gender = "M"
                worksheet.write(i, 12, gender.upper)
                worksheet.write(i, 13, affiliate.document_id.upper)
                worksheet.write(i, 14, affiliate.position.upper)
                worksheet.write(i, 15, "")
                i += 1
            workbook.close()
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment;filename="Censo_'+str(year)+'.xlsx"'
            response.write(output.getvalue())
            return response
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
# Refactor to ViewSets after this point

class AffiliateViewSet(viewsets.ModelViewSet):
    permission_classes = [EntityAdminPermission]
    serializer_class = AffiliateSerializer
    queryset = Affiliate.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(entity=self.request.user.entity, active=True)

    def perform_create(self, serializer):
        serializer.save(entity=self.request.user.entity)
    
    def list(self, request, *args, **kwargs):
        if not request.user.is_entity_admin:
            serializer = self.get_serializer(super().get_queryset(), fields=Affiliate.fields_limited, many=True)
            return Response(serializer.data)
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_entity_admin:
            serializer = self.get_serializer(self.get_object(), fields=Affiliate.fields_limited)
            return Response(serializer.data)
        return super().retrieve(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data={'active':False}, partial=True)
        if serializer.is_valid():
            serializer.save(active=False)
        else:
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class PaymentChoicesViewSet(mixins.CreateModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [IsUserOwner]
    serializer_class = PaymentChoiceSerializer
    queryset = PaymentChoice.objects.all()
