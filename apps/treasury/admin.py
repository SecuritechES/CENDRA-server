from django.contrib import admin
from .models import BankAccount, Income, Outcome

admin.site.register(BankAccount)
admin.site.register(Income)
admin.site.register(Outcome)