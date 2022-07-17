from rest_framework import serializers
from .models import Record

class RecordSerializer(serializers.ModelSerializer):
	class Meta:
		model=Record
		fields=['points','difficulty','timer','life','date','user']
		#if you want to include all the fields in the model then fields=__all__
		extra_kwargs = {"user": {"required": False}}