import re
import os
from django.db import models
from django.core.exceptions import ValidationError
from apps.entity.models import Directorate

class Affiliate(models.Model):
    def photo_upload_rename(instance, filename):
        _, ext = os.path.splitext(filename)
        path = 'avatar/user/{0}'.format(instance.id)
        return 'avatar/user/{0}/{1}'.format(instance.id, "photo" + ext)

    class DocumentType(models.IntegerChoices):
        DNI = 1, "DNI"
        NIE = 2, "NIE"
        PAS = 3, "Pasaporte"
    class Gender(models.TextChoices):
        MALE = "M", "Hombre"
        FEMALE = "F", "Mujer"

    entity = models.ForeignKey('entity.Entity', on_delete=models.CASCADE, null=True)
    census_number = models.IntegerField(blank=True, null=True)
    jcf_number = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    document_type = models.IntegerField(choices=DocumentType.choices, default=DocumentType.DNI)
    document_id = models.CharField(max_length=9)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=9, blank=True)
    photo = models.ImageField(default="/default_photo.png", upload_to=photo_upload_rename)
    birthday = models.DateField()
    gender = models.CharField(max_length=9, choices=Gender.choices, default=Gender.MALE)
    address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="España")
    has_legal_tutor = models.BooleanField(default=False)
    legal_tutor = models.ForeignKey('self', on_delete=models.RESTRICT, null=True, blank=True, related_name='tutor')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('census_number', 'pk')

    def __str__(self):
        return str(self.name + " " + self.surnames)
    
    @property
    def position(self):
        try:
            position = Directorate.objects.get(user=self.id)
        except Directorate.DoesNotExist:
            position = None
        if position is None:
            return 'Vocal'
        return position.position.name

class PaymentChoice(models.Model):
    def validate_iban(value):
        """
        Validator function that checks if the given value is a valid IBAN number.
        """
        iban_regex = r'^[A-Z]{2}\d{2}[A-Z\d]{4}\d{10}$'
        if not re.match(iban_regex, value):
            raise ValidationError('Invalid IBAN number')
        
    class PaymentType(models.IntegerChoices):
        CASH = 1, "Efectivo"
        DOMICILATION = 2, "Domiciliación bancaria"
        TRANSFER = 3, "Transferencia bancaria"

    affiliate = models.OneToOneField('Affiliate', on_delete=models.CASCADE, related_name='payment_choice')
    payment_type = models.IntegerField(choices=PaymentType.choices, default=PaymentType.CASH)
    account_holder = models.CharField(max_length=100, null=True, blank=True)
    account_iban = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.payment_type)