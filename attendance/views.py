from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import AttendanceFile,Attendance
from employee.models import User
from .forms import UploadFileForm

class PassRequestToFormViewMixin:
	def get_form_kwargs(self):
		kwargs = super(PassRequestToFormViewMixin, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

class AttendanceFileListView(LoginRequiredMixin,ListView):
	model = AttendanceFile
	paginate_by = 50

	def get_queryset(self):
		attendance = AttendanceFile.objects.all().order_by('-created_date')
		return attendance

class AttendanceFileDetailView(PermissionRequiredMixin,LoginRequiredMixin,DetailView):
	model = AttendanceFile
	permission_required = ('attendance.import_attendance_file','attendance.process_attendance_file')


class AttendanceFileDeleteView(PermissionRequiredMixin,LoginRequiredMixin,DeleteView):
	model = AttendanceFile
	success_url = reverse_lazy('attendance:list')
	permission_required = ('attendance.import_attendance_file','attendance.process_attendance_file')

class AttendanceFileCreate(PermissionRequiredMixin,LoginRequiredMixin,CreateView):
	model 		= AttendanceFile
	form_class 	= UploadFileForm
	success_url = reverse_lazy('attendance:list')
	permission_required = ('attendance.import_attendance_file','attendance.process_attendance_file')

	def get_context_data(self, **kwargs):
		context = super(AttendanceFileCreate, self).get_context_data(**kwargs)        
		context['title'] = 'Upload Attendance log file'
		context['next'] = self.request.GET.get('next')
		return context

def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None

def process_file(request,pk):
	import datetime
	from django.utils import timezone
	from datetime import timedelta
	print ('Start process file :%s' % pk )
	fileObj = AttendanceFile.objects.get(pk=pk)
	f= fileObj.filename
	f.open(mode='rb') 
	lines = f.readlines()
	f.close()
	for line in lines:
		i = line.decode("utf-8").split('  ')
		en=i[0]
		stamp_date	 = datetime.datetime.strptime(i[1], "%d-%m-%Y").date()
		
		# First filter , accept only attendance time > now -1 month
		if stamp_date < timezone.now().date()- timedelta(days=31) :
			continue

		stamp_time	 = datetime.datetime.strptime(i[2], "%H:%M").time()
		source 		 = i[3]
		fn 			 = i[4]
		user 		= get_or_none(User,en=en)
		
		# Second filter ,check En existing in system.
		if user == None:
			continue

		obj, created = Attendance.objects.get_or_create(
				    user = user,
				    stamp_date = stamp_date,
					stamp_time = stamp_time,
					stamp_datetime = datetime.datetime.combine(stamp_date,stamp_time),
					defaults={'stamp_status': fn ,
								'source': source,
								'attendancefile': fileObj}
				)
	fileObj.uploaded = True
	fileObj.uploaded_date = timezone.now().date()
	fileObj.save()
	url = reverse_lazy('attendance:list')
	return HttpResponseRedirect(url)

		# if created :
		# 	print ('New record: %s' % obj)
		# defaults={'birthday': date(1940, 10, 9)}

		# else:
		# 	print ('%s - %s - %s'%(i[0],stamp_date,stamp_time))


