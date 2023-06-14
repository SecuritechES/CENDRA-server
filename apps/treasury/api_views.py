import logging
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import BankAccount, Income, Outcome
from .serializers import BankAccountSerializer, IncomeSerializer, OutcomeSerializer

class BankAccounts(APIView):
    @swagger_auto_schema(responses={200: BankAccountSerializer})
    def get(self, request, *args, **kwargs):
        """
        Retrieves the BankAccounts. 

        If successful, returns an array of objects.
        """
        accounts = BankAccount.objects.filter(entity=request.user.entity.id)
        serializer = BankAccountSerializer(accounts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Creates a new Bank Account for the current user entity.

        If successful, returns the created bank account as a JSON object.
        """
        serializer = BankAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(entity=request.user.entity)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class Transactions(APIView):
    def get(self, request, *args, **kwargs):
        account_id = self.request.query_params.get('account')
        account = get_object_or_404(BankAccount, pk=account_id, entity=request.user.entity)
        incomes = Income.objects.filter(account=account)
        outcomes = Outcome.objects.filter(account=account)
        income_serializer = IncomeSerializer(incomes, many=True)
        outcome_serializer = OutcomeSerializer(outcomes, many=True)
        transactions = {'incomes': income_serializer.data, 'outcomes': outcome_serializer.data}
        return Response(transactions)
