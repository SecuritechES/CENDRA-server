import os
from django.db import models

class Entity(models.Model):
    def logo_upload_rename(instance, filename):
        _, ext = os.path.splitext(filename)
        return 'avatar/entity/{0}/{1}'.format(instance.id, "logo" + ext)

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=9, blank=True)
    email = models.EmailField(blank=True)
    logo = models.ImageField(default="/default_logo.png", upload_to=logo_upload_rename)
    business_name = models.CharField(max_length=100, blank=True)
    nif = models.CharField(max_length=9, blank=True)
    registry_number = models.CharField(max_length=100, blank=True)
    social_address = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default="España")
    is_same_address = models.BooleanField(default=True)
    fiscal_address = models.CharField(max_length=100, blank=True)
    fiscal_postal_code = models.CharField(max_length=5, blank=True)
    fiscal_city = models.CharField(max_length=100, blank=True)
    fiscal_province = models.CharField(max_length=100, blank=True)
    fiscal_country = models.CharField(max_length=100, blank=True)
    join_password = models.CharField(max_length=20, blank=True)

    def save(self, *args, **kwargs):
        # If "is_same_address" equals True, fiscal data is equal to social data
        if self.is_same_address:
            self.fiscal_address = self.social_address
            self.fiscal_postal_code = self.postal_code
            self.fiscal_city = self.city
            self.fiscal_province = self.province
            self.fiscal_country = self.country
        super(Entity, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

class DirectoratePosition(models.Model):
    name = models.CharField(max_length=100)
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE, related_name='positions')
    priority = models.IntegerField()

    def __str__(self):
        return str(self.name)

class Directorate(models.Model):
    user = models.OneToOneField('affiliate.Affiliate', on_delete=models.CASCADE)
    position = models.ForeignKey('DirectoratePosition', on_delete=models.PROTECT)
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE)

class YearlyCensusEntry(models.Model):
    affiliate = models.ForeignKey('affiliate.Affiliate', on_delete=models.SET_NULL, null=True)
    jcf_number = models.IntegerField(blank=True, null=True)
    census_number = models.IntegerField(blank=True, null=True)
    commission = models.CharField(max_length=100)
    surnames = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=5)
    phone = models.CharField(max_length=9, blank=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=1)
    document_id = models.CharField(max_length=20) 
    position = models.CharField(max_length=100)
    reward = models.CharField(max_length=100)

    def __str__(self):
        return self.surnames + ", " + self.name

class YearlyCensus(models.Model):
    entity = models.ForeignKey('Entity', on_delete=models.CASCADE)
    entries = models.ManyToManyField(YearlyCensusEntry)
    year = models.IntegerField()

    def __str__(self):
        return "Censo " + str(self.year)