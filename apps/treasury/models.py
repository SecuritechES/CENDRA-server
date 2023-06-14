from django.db import models
import re
from django.core.exceptions import ValidationError

class BankAccount(models.Model):
    def validate_iban(value):
        """
        Validator function that checks if the given value is a valid IBAN number.
        """
        iban_regex = r'^[A-Z]{2}\d{2}[A-Z\d]{4}\d{10}$'
        if not re.match(iban_regex, value):
            raise ValidationError('Invalid IBAN number')
    
    entity = models.ForeignKey('entity.Entity', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    iban = models.CharField(max_length=100, null=True, blank=True, validators=[validate_iban])
    initial_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

    @property
    def balance(self):
        incomes = Income.objects.filter(account=self.id).aggregate(models.Sum('amount'))['amount__sum']
        outcomes = Outcome.objects.filter(account=self.id).aggregate(models.Sum('amount'))['amount__sum']
        if incomes is None:
            incomes = 0
        if outcomes is None:
            outcomes = 0
        return self.initial_amount + incomes + outcomes

class Income(models.Model):
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
    concept = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Outcome(models.Model):
    account = models.ForeignKey('BankAccount', on_delete=models.CASCADE)
    concept = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
