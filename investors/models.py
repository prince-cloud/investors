from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse
# Create your models here.


class Investor(models.Model):
    SEX_CHOICES = (
        ("M", "M"),
        ("F", "F"),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=2)
    phone = models.CharField(max_length=10)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country_to_invest = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)
        
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name