# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


# Create your models here.
class ContactDetail(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    street_address1 = models.CharField(max_length=50, blank=True, null=True)
    street_address2 = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=40, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    town_or_city = models.CharField(max_length=40, blank=True, null=True)
    country = CountryField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Passenger(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=False)
    citizenship = CountryField()
    passport_id = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
