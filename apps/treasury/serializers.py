from rest_framework import serializers
from .models import BankAccount, Income, Outcome

class BankAccountSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=6, decimal_places=2)

    def get_balance(self, instance):
        return self.get_balance
    
    class Meta:
        model = BankAccount
        fields = [
            'id',
            'name',
            'iban',
            'initial_amount',
            'balance'
        ]

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        exclude = ['account']

class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome
        exclude = ['account']