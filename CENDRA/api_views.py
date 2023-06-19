from rest_framework.views import APIView
from rest_framework.response import Response
from apps.affiliate.models import Affiliate
from apps.treasury.models import BankAccount, Income, Outcome
from apps.treasury.serializers import BankAccountSerializer
from apps.news.models import NewsItem

class Dashboard(APIView):
    def get(self, request, *args, **kwargs):
        """
        Returns basic information about the entity status.
        
        """
        name = request.user.affiliate.name
        members = Affiliate.objects.filter(entity=request.user.entity).count()
        news = NewsItem.objects.filter(entity=request.user.entity).count()
        bank = BankAccount.objects.filter(entity=request.user.entity.id)
        bank_serializer = BankAccountSerializer(bank, many=True)
        
        transactions_count = 0
        incomes = Income.objects.filter(account__entity=request.user.entity).count()
        outcomes = Outcome.objects.filter(account__entity=request.user.entity).count()
        transactions_count = incomes + outcomes

        return Response({'name': name, 'members': members, 'news': news, 'bank_accounts': bank_serializer.data, 'movements': transactions_count})
