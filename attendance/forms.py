from django.forms import ModelForm,Textarea
from django import forms

from .models import AttendanceFile

class UploadFileForm(ModelForm):
	class Meta:
		model = AttendanceFile
		fields = ['filename','description']
		widgets = {
            'description': Textarea(attrs={'cols': 50, 'rows': 3}),
   			}