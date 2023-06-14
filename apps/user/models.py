from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save

class CendraUser(AbstractUser):
    class OnboardingStatus(models.IntegerChoices):
        ENTITY_SETUP =  0
        AFFILIATE_SETUP = 1
        COMPLETED = 99

    entity = models.ForeignKey('entity.Entity', on_delete=models.CASCADE, null=True, blank=True)
    is_entity_admin = models.BooleanField(default=False)
    affiliate = models.OneToOneField('affiliate.Affiliate', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField('email address', unique=True)
    onboarding = models.IntegerField(choices=OnboardingStatus.choices, default=OnboardingStatus.ENTITY_SETUP)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
