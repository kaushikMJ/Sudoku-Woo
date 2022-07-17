from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Record(models.Model):
	points=models.IntegerField(default=0)
	difficulty=models.TextField()
	date = models.DateTimeField(blank=True,auto_now_add=True) 
	timer=models.TextField(max_length=8)
	life=models.IntegerField(default=0)
	user=models.ForeignKey(User, on_delete=models.CASCADE)


	def __str__(self):
		return self.date

