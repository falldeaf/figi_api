import datetime
from django.db import models
from django.utils import timezone

class Cusips(models.Model):
	cusip_code = models.CharField(max_length=9, unique=True)
	ticker = models.CharField(max_length=20, blank=True, null=True)
	entity_name = models.CharField(max_length=100, blank=True, null=True)
	market_sector = models.CharField(max_length=15)
	security_type = models.CharField(max_length=15)
	exchange_code = models.CharField(max_length=15, blank=True, null=True)
	timestamp = models.DateTimeField('cusip_date')
	def __str__(self):
		return self.cusip_code + " : " + self.entity_name + " : " +  self.market_sector