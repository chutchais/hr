from rest_framework import serializers
from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from company.models import Company



class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['name','description','url']

