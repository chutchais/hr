from django.forms import ModelForm,Textarea
from django import forms
from .models import Working
import datetime

class WorkingForm(ModelForm):
	working_date = forms.CharField(disabled=True)
	next 		 = forms.CharField(widget=forms.HiddenInput(),required=False,disabled=True)
	# user = forms.CharField(disabled=True)
	def __init__(self, *args, **kwargs):
		self.request = kwargs.pop("request")
		super(WorkingForm, self).__init__(*args, **kwargs)
		# self.fields['working_date'] = datetime.date(2019,2,16)
		

	class Meta:
		model = Working
		fields = ['user','working_date','workingcode','note']
		widgets = {
            'note': Textarea(attrs={'cols': 50, 'rows': 3}),
   			}

	def clean(self):
		# workingcode = self.cleaned_data.pop('workingcode')
		print('clean')

class UploadFileForm(forms.Form):
	# filetype = forms.ModelChoiceField(queryset= FileType.objects.filter(status='A'), empty_label="(Please select File Type)")
	file = forms.FileField()
