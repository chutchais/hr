from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
# Create your views here.
from .models import Working,WorkingCode
from .forms import WorkingForm,UploadFileForm
from department.models import Department
from employee.models import User
from department.models import Section
import datetime
from django.urls import reverse
import xlrd
import calendar


from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class PassRequestToFormViewMixin:
	def get_form_kwargs(self):
		kwargs = super(PassRequestToFormViewMixin, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

class WorkingCreate(PassRequestToFormViewMixin,LoginRequiredMixin,CreateView):
	model 		= Working
	form_class 	= WorkingForm
	success_url = reverse_lazy('schedule:list')

	def get_form_kwargs(self, **kwargs):
		kwargs = super(WorkingCreate, self).get_form_kwargs()
		redirect = self.request.GET.get('next')
		print ('get_form_kwargs %s' % redirect )
		if redirect:
			if 'initial' in kwargs.keys():
				kwargs['initial'].update({'next': redirect})
			else:
				kwargs['initial'] = {'next': redirect}
		return kwargs


	def get_form(self, form_class=None):
		"""
		Returns an instance of the form to be used in this view.
		"""
		form = super(WorkingCreate, self).get_form(form_class)
		# user = Section.objects.get(name=self.kwargs['section'])
		form.fields['workingcode'].queryset = WorkingCode.objects.filter(section__name=self.kwargs['section'])
		form.fields['user'].queryset = User.objects.filter(en=self.kwargs['en'])
		return form

	def get_initial(self):
		# print ('CreateView-get_initial')
		initial = super().get_initial()
		# cpf - it's the name of the field on your current form
		# self.args will be filled from URL. I'd suggest to use named parameters
		# so you can access e.g. self.kwargs['cpf_initial']
		year = self.request.GET.get('year', None)
		month = self.request.GET.get('month', None)
		day = self.request.GET.get('day', None)
		initial['working_date'] = datetime.date(int(year),int(month),int(day))
		initial['user'] = User.objects.get(en =self.kwargs['en'])
		# initial['next'] = self.request.GET.get('next', None)
		# print (initial)
		return initial

	def form_valid(self, form):
		# form.instance.user = self.request.user
		# print ('On form_valid %s' % self.request.user)
		s = super(WorkingCreate, self).form_valid(form)
		form.instance.logs.create(note= ('[ work code : %s] %s ' %(form.instance.workingcode.name,form.instance.note)) ,
							user=self.request.user,log_type='DRAFT')
		redirect = form.cleaned_data.get('next')
		print ('form valid %s' % redirect )
		if redirect:
			self.success_url = redirect
		s = super(WorkingCreate, self).form_valid(form)
		return s

	def get_context_data(self, **kwargs):
		context = super(WorkingCreate, self).get_context_data(**kwargs)        
		# year = self.request.GET.get('year', None)
		# month = self.request.GET.get('month', None)
		# day = self.request.GET.get('day', None)
		# context['working_date'] = datetime.date(int(year),int(month),int(day))
		context['title'] = 'Create Working Schedule'
		context['next'] = self.request.GET.get('next')
		return context

class WorkingUpdate(PassRequestToFormViewMixin,UpdateView):
	model = Working
	form_class 	= WorkingForm
	# fields = ['workingcode','note']
	pk_url_kwarg = 'pk'
	success_url = reverse_lazy('schedule:list')
	
	def get_form_kwargs(self, **kwargs):
		kwargs = super(WorkingUpdate, self).get_form_kwargs()
		redirect = self.request.GET.get('next')
		print ('get_form_kwargs %s' % redirect )
		if redirect:
			if 'initial' in kwargs.keys():
				kwargs['initial'].update({'next': redirect})
			else:
				kwargs['initial'] = {'next': redirect}
		return kwargs

	def get_context_data(self, **kwargs):
		context = super(WorkingUpdate, self).get_context_data(**kwargs)        
		context['title'] = 'Update Working Schedule'
		context['next'] = self.request.GET.get('next')
		return context

	def get_form(self, form_class=None):
		"""
		Returns an instance of the form to be used in this view.
		"""
		self.object = self.get_object()
		form = super(WorkingUpdate, self).get_form(form_class)
		# print (self.object.user.section)
		form.fields['workingcode'].queryset = WorkingCode.objects.filter(section=self.object.user.section)
		return form

	def form_valid(self, form):
		# form.instance.user = self.request.user
		# print ('On form_valid %s' % self.request.user)
		s = super(WorkingUpdate, self).form_valid(form)
		form.instance.logs.create(note= ('[ work code : %s] %s ' %(form.instance.workingcode.name,form.instance.note)) ,
							user=self.request.user,log_type='CHANGE')
		redirect = form.cleaned_data.get('next')
		print ('form valid %s' % redirect )
		if redirect:
			self.success_url = redirect
		s = super(WorkingUpdate, self).form_valid(form)
		return s

class WorkingDelete(DeleteView):
	model = Working
	success_url = reverse_lazy('schedule:list')

class WorkingListView(LoginRequiredMixin,ListView):
	model = Working
	# template_name = 'schedule/bayplan_voy_detail.html'

	def get_context_data(self, **kwargs):
		context     = super().get_context_data(**kwargs)
		user 		= self.request.user
		section 	= user.section
		department 	= section.department
		# print(user.groups.all())
		year = self.request.GET.get('year', None)
		month = self.request.GET.get('month', None)

		# display mode (mode=None --> show Working Code(default) , mode=Status -->show status mode)
		mode = self.request.GET.get('mode', None)

		if year and month:
			report_date 	= datetime.date(int(year),int(month),1)
		else:
			report_date 	= timezone.now()

		context['now'] 	= report_date

		if user.groups.filter(name__in=['HR staff']).exists():
			# print ('HR Staff')
			if 'department' in self.kwargs:
				department 	= self.kwargs['department']
				# print (department)
				context['section_list'] = list(Section.objects.filter(department__name = department))
				context['working_list'] = list(Working.objects.filter(
										user__section__department__name = department,
										working_date__year = report_date.year,
										working_date__month = report_date.month))
				context['department'] = department
				print('finished on View')
			else:
				context['section_list'] 	= None
				context['working_list'] 	= None

			context['department_list']	= list(Department.objects.all())
			context['hr_staff']			= True
		else :
			# show nothing in first time, must select Section
			context['section_list'] 	= None
			context['working_list'] 	= None
			context['section_list'] = list(Section.objects.filter(name = section.name))
			context['working_list'] = list(Working.objects.filter(
										user__section = section,
										working_date__year = report_date.year,
										working_date__month = report_date.month))
			# context['section_list'] = list(Section.objects.filter(department = section.department))
			# context['working_list'] = list(Working.objects.filter(
			# 							user__section__department = department,
			# 							working_date__year = report_date.year,
			# 							working_date__month = report_date.month))
		if mode :
			context['mode'] = mode

		
		return context

	# def get_queryset(self):
	# 	user 		= self.request.user
	# 	section 	= user.section
	# 	department 	= section.department
	# 	if user.groups.filter(name__in=['HR staff']).exists():
	# 		working = Working.objects.all()
	# 	else:
	# 		working = Working.objects.filter(user__section__department = department)
	# 	return working

class WorkingSectionListView(LoginRequiredMixin,ListView):
	model = Working
	# self.kwargs['lab']
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['department'] ='TEst depart'
		user 		= self.request.user
		section 	= user.section
		context['now'] = timezone.now()
		context['section_list'] = Section.objects.filter(department = section.department)
		return context

# Working Status view
class WorkingStatusListView(LoginRequiredMixin,ListView):
	model = Working
	template_name ='schedule/status_list.html'

	def get_context_data(self, **kwargs):
		context 			= super().get_context_data(**kwargs)
		context['status'] 	= self.kwargs['status']
		return context

	def get_queryset(self):
		user 		= self.request.user
		section 	= user.section
		department 	= section.department
		if 'status' in self.kwargs:
			status 	= self.kwargs['status']

		if user.groups.filter(name__in=['HR staff']).exists():
			working = Working.objects.filter(status=status).order_by('working_date')
		else:
			working = Working.objects.filter(status=status,user__section__department = department).order_by('working_date')
		print ('Status-Code:%s' % status)
		return working

def ProcessWorking(request,pk,action):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	
	print (pk,action)
	url = request.GET.get('next')

	# Process ,move to next process
	working = Working.objects.get(pk=pk)
	working.status = action
	working.save()
	# Log
	if action == 'PRE_APPROVE':
		action = 'START'
	if action == 'APPROVE':
		action = 'PRE_APPROVE'
	if action == 'ACKNOWLEDGE':
		action = 'APPROVE'
	working.logs.create(note= ('[ work code : %s]' %(working.workingcode.name)) ,
							user=request.user,log_type=action)
	print('Process Done')



	# slug = c.bayplanfile.slug
	# bay = c.bay

	# mode = request.GET.get('mode')
	# view = request.GET.get('view')
	# pos = request.GET.get('pos')
	# if mode=='search':
	# 	query = request.GET.get('q')
	# 	url = reverse('container:bay',kwargs={'slug':slug})
	# 	url = '%s?q=%s&view=%&pos=%s' % (url , query,view,pos)
	# else:
	# 	url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
	# 	url = '%s?q=%s&view=%s&pos=%s' % (url , c.container,view,pos)

	return HttpResponseRedirect(url)


def import_working_data(request):
	working_month = timezone.now()
	section = None
	working_list = []
	if request.method == "POST":
		form = UploadFileForm(request.POST, request.FILES)
		working_month = timezone.now()
		if form.is_valid():
			# print(request.FILES['file'].name)
			working_month,section,working_list=get_working_from_sheet(request,request.FILES['file'])
			# filehandle = request.FILES['file']
			# book = xlrd.open_workbook(file_contents=filehandle.read())
			# print ('Upload Okay')
			# xl_sheet = book.sheet_by_index(0)
			# data_start = False
			# employee_list = []
			# working_list = []
			# d={}
			# for row_index in range(0, xl_sheet.nrows):
			# 	vCell 			= xl_sheet.cell(row_index, 0).value.__str__().strip()
			# 	# vCellValue	 	= xl_sheet.cell(row_index, 1).value.__str__().strip()
			# 	if vCell == 'year' or vCell=='Year':
			# 		year = xl_sheet.cell(row_index, 1).value
			# 		continue
			# 	if vCell == 'month' or vCell=='Month':
			# 		month = xl_sheet.cell(row_index, 1).value
			# 		working_month = datetime.date(int(year),int(month),1)
			# 		print (working_month)
			# 		continue
			# 	if vCell == 'department' or vCell=='Department':
			# 		department_str = xl_sheet.cell(row_index, 1).value.__str__().strip()
			# 		continue
			# 	if vCell == 'section' or vCell=='Section':
			# 		section_str = xl_sheet.cell(row_index, 1).value.__str__().strip()
			# 		# get section object
			# 		section = Section.objects.get(name=section_str,department__name=department_str)
			# 		# section_list = list(section)
			# 		# print (section)
			# 		continue
			# 	if vCell == 'name' or vCell=='Name':
			# 		data_start = True
			# 		continue

			# 	if data_start:
			# 		number_of_day = calendar.monthrange(working_month.year,working_month.month)[1]
			# 		d={'name':'',
			# 			'en':''}
			# 		em_name = vCell
			# 		em_en 	= xl_sheet.cell(row_index, 1).value.__str__().strip().replace('.0','')
			# 		d['name'] = em_name
			# 		d['en']  = em_en
					
			# 		emp = User.objects.get(en=em_en)
			# 		# working_code = WorkingCode.objects.get(name='D1',section=section)
					
			# 		# print(working)

			# 		# employee_list.append(emp)

			# 		for i in range(1,number_of_day+1):
			# 			# print (working_month.replace(day=i))
			# 			# working_code = WorkingCode.objects.get(name='D1',section=section)
			# 			code = xl_sheet.cell(row_index, i+1).value.__str__().strip().replace('.0','')
			# 			workingcode = WorkingCode.objects.get(name=code,section=section)
			# 			working = Working(user=emp,
			# 								working_date=working_month.replace(day=i),
			# 								workingcode=workingcode)
			# 			# print(working)
			# 			working_list.append(working)
			# 		# print (employee_list)
			# 		# Loop for each day

			



			# print (year,month,department_str,section_str)
				# for col_index in range(xl_sheet.ncols):
				# 	vCell = xl_sheet.cell(row_index, col_index).value.__str__().strip()
				# 	print (vCell)

			# return excel.make_response(filehandle.get_sheet(), "csv",
			#                            file_name="download")
	else:
		form = UploadFileForm()
	return render(
		request,
		'schedule/working_upload_form.html',
		{
			'form': form,
			'now' : working_month,
			'section':section,
			'working_list' : working_list,
			'title': 'Excel file upload',
		})

def confirm_working(request):
	import math
	rows = request.POST.get('rows', '')
	# from django.utils import six 
	# post_dict = dict(six.iterlists(rows))
	# import ast
	# datas = ast.literal_eval(rows)
	# print(rows)
	for x in rows:
		print(x)
	# for i,r in enumerate(datas):
	# 	print('index %s -- %s' % (i,r.user))


def get_working_from_sheet(request,filehandle):
	# filehandle = request.FILES['file']
	book = xlrd.open_workbook(file_contents=filehandle.read())
	print ('Upload Okay')
	xl_sheet = book.sheet_by_index(0)
	data_start = False
	employee_list = []
	working_list = []
	d={}
	for row_index in range(0, xl_sheet.nrows):
		vCell 			= xl_sheet.cell(row_index, 0).value.__str__().strip()
		# vCellValue	 	= xl_sheet.cell(row_index, 1).value.__str__().strip()
		if vCell == 'year' or vCell=='Year':
			year = xl_sheet.cell(row_index, 1).value
			continue
		if vCell == 'month' or vCell=='Month':
			month = xl_sheet.cell(row_index, 1).value
			working_month = datetime.date(int(year),int(month),1)
			print (working_month)
			continue
		if vCell == 'department' or vCell=='Department':
			department_str = xl_sheet.cell(row_index, 1).value.__str__().strip()
			continue
		if vCell == 'section' or vCell=='Section':
			section_str = xl_sheet.cell(row_index, 1).value.__str__().strip()
			# get section object
			section = Section.objects.get(name=section_str,department__name=department_str)
			# section_list = list(section)
			# print (section)
			continue
		if vCell == 'name' or vCell=='Name':
			data_start = True
			continue

		if data_start:
			number_of_day = calendar.monthrange(working_month.year,working_month.month)[1]
			d={'name':'',
				'en':''}
			em_name = vCell
			em_en 	= xl_sheet.cell(row_index, 1).value.__str__().strip().replace('.0','')
			d['name'] = em_name
			d['en']  = em_en
			
			emp = User.objects.get(en=em_en)
			# working_code = WorkingCode.objects.get(name='D1',section=section)
			
			# print(working)

			# employee_list.append(emp)

			for i in range(1,number_of_day+1):
				# print (working_month.replace(day=i))
				# working_code = WorkingCode.objects.get(name='D1',section=section)
				code = xl_sheet.cell(row_index, i+1).value.__str__().strip().replace('.0','')
				workingcode = WorkingCode.objects.get(name=code,section=section)
				working = Working(user=emp,
									working_date=working_month.replace(day=i),
									workingcode = workingcode)

				# if created :
				# 	working.workingcode = workingcode
				# 	working.save()
				# 	working.logs.create(note= ('[ work code : %s] %s ' %(code,'By uploading..')) ,
				# 			user=request.user,log_type='DRAFT')
				# 	print ('%s -->New data' % working)
					
				# else:
				# 	if working.workingcode != workingcode :
				# 		working.workingcode = workingcode
				# 		working.save()
				# 		working.logs.create(note= ('[ work code : %s] %s ' %(code,'Modify Working Code')) ,
				# 			user=request.user,log_type='DRAFT')
				# 		print ('%s -->Change Workingcode' % working)

				# if working.workingcode != workingcode :
				# 	print ('%s change code from %s to %s ' % (working,working.workingcode,workingcode))
				
				# working.workingcode = workingcode
				# working.save()


					
				# working.save()
				# print(working)
				working_list.append(working)

			Working.objects.bulk_create(working_list)
	return working_month,section,working_list