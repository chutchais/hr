from django.forms import ModelForm
from django import forms
from .models import Working
import datetime

class WorkingForm(ModelForm):
	working_date = forms.CharField(disabled=True)
	# user = forms.CharField(disabled=True)
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(WorkingForm, self).__init__(*args, **kwargs)
		# self.fields['working_date'] = datetime.date(2019,2,16)
		

	class Meta:
		model = Working
		fields = ['user','working_date','workingcode','note']

	def clean(self):
		# workingcode = self.cleaned_data.pop('workingcode')
		print('clean')
