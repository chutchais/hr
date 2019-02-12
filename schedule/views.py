from django.shortcuts import render

from django.shortcuts import get_object_or_404
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
# Create your views here.
from .models import Working,WorkingCode
from .forms import WorkingForm
from employee.models import User
from department.models import Section
import datetime


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
        print ('CreateView-get_initial')
        initial = super().get_initial()
        # cpf - it's the name of the field on your current form
        # self.args will be filled from URL. I'd suggest to use named parameters
        # so you can access e.g. self.kwargs['cpf_initial']
        year = self.request.GET.get('year', None)
        month = self.request.GET.get('month', None)
        day = self.request.GET.get('day', None)
        initial['working_date'] = datetime.date(int(year),int(month),int(day))
        initial['user'] = User.objects.get(en =self.kwargs['en'])
        return initial

    def form_valid(self, form):
        # form.instance.user = self.request.user
        return super(WorkingCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(WorkingCreate, self).get_context_data(**kwargs)        
        # year = self.request.GET.get('year', None)
        # month = self.request.GET.get('month', None)
        # day = self.request.GET.get('day', None)
        # context['working_date'] = datetime.date(int(year),int(month),int(day))
        context['title'] = 'Create Working Schedule'
        return context

class WorkingUpdate(UpdateView):
    model = Working
    fields = ['workingcode','note']
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('schedule:list')
    
    def get_context_data(self, **kwargs):
        context = super(WorkingUpdate, self).get_context_data(**kwargs)        
        context['title'] = 'Update Working Schedule'
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

class WorkingDelete(DeleteView):
    model = Working
    success_url = reverse_lazy('schedule:list')

class WorkingListView(LoginRequiredMixin,ListView):
	model = Working
	# template_name = 'schedule/bayplan_voy_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user 		= self.request.user
		section 	= user.section
		department 	= section.department

		year = self.request.GET.get('year', None)
		month = self.request.GET.get('month', None)

		if year and month:
			report_date 	= datetime.date(int(year),int(month),1)
		else:
			report_date 	= timezone.now()

		context['now'] 	= report_date

		context['section_list'] = list(Section.objects.filter(department = section.department))
		context['working_list'] = list(Working.objects.filter(
										user__section__department = department,
										working_date__year = report_date.year,
										working_date__month = report_date.month))

		return context

	def get_queryset(self):
		user 		= self.request.user
		section 	= user.section
		department 	= section.department
		return Working.objects.filter(user__section__department = department)

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
