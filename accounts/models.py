from django.db import models
from django.contrib.auth.models import AbstractUser

JOB_CHOICES = (
	('programmer','Programmer'),
	('Doctor','Doctor'),
	('Taxi_Driver','taxi_driver'),
	('Engineer','engineer'),
	('Other','other'),
)

class CustomUser(AbstractUser):
	phone_number = models.CharField(blank=False, null=False, max_length=11, unique=True)
	job = models.CharField(blank=True, null=True, choices=JOB_CHOICES, default='programmer')

	


