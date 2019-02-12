from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.contrib.auth.models import User
from django import forms
# Register your models here.
from schedule.models import WorkingCode,Working
from employee.models import Section,User

class WorkingCodeAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = ['name','start_time','end_time','section']
    list_display = ('name','color','start_time','end_time','section','dayoff','active')
    list_editable = ('color','start_time','end_time',)
    fieldsets = [
        ('Basic Information',{'fields': ['name','section','description','color']}),
        ('Time Information',{'fields': [('start_time','end_time'),'dayoff']}),
        ('General Information',{'fields': ['active']}),

    ]
admin.site.register(WorkingCode,WorkingCodeAdmin)



class WorkingDateListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Working Date range')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'working_date'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('today', _('Today')),
            ('yesterday', _('Yesterday')),
            ('tomorrow', _('Tomorrow')),
            ('thisweek', _('This week')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        from datetime import date
        import datetime
        if self.value() == 'today':
            today = date.today()
            return queryset.filter(working_date=today)

        if self.value() == 'yesterday':
            yesterday = date.today() - datetime.timedelta(days=1)
            return queryset.filter(working_date=yesterday)

        if self.value() == 'tomorrow':
            tomorrow = date.today() + datetime.timedelta(days=1)
            return queryset.filter(working_date=tomorrow)

        if self.value() == 'thisweek':
            
            date = datetime.date.today()
            start_week = date - datetime.timedelta(date.weekday())
            end_week = start_week + datetime.timedelta(7)
            return queryset.filter(working_date__range=[start_week, end_week])

class SectionListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Sections')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'section'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # print(self.value())
        if not request.user.is_superuser :
            department = request.user.section.department
            queryset = Section.objects.filter(department = department).order_by('department','name')
        else:
            queryset = Section.objects.all().order_by('department','name')
        
        list_of_sections = []
        for section in queryset:
            list_of_sections.append(
                (str(section.name), section.name)
            )
        return sorted(list_of_sections, key=lambda tp: tp[1])

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        # self.request = request
        # print (request.user.is_superuser)
        if request.user.is_superuser:
            return queryset.all().order_by('-working_date')

        if not self.value() is None :
            print ('click on %s' % self.value())
            section = self.value()
            return queryset.filter(user__section = section).order_by('-working_date')


def get_en(self):
    return self.user.en
get_en.short_description = 'EN number'  #Renames column head

def get_section(self):
    return self.user.section
get_section.short_description = 'Section'  #Renames column head

def get_color(self):
    return self.workingcode.color
get_color.short_description = 'Code'  #Renames column head

def status_colored(self):
    color 		= self.workingcode.color
    code_name 	= self.workingcode.name
    return format_html(
            '<b style="background:{};">{}</b>',
            color,
            code_name
                       )
status_colored.admin_order_field = 'Color'

class WorkingForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request', None)
        instance = kwargs.get('instance', None)
        super (WorkingForm,self ).__init__(*args,**kwargs) # populates the post
        # print ('init on WorkingForm %s' % self.current_user.username)
        department = self.current_user.section.department
        self.fields['user'].queryset = User.objects.filter(section__department = department)
        # print (instance.workingcode.section)
        if instance :
            # Show only working code of user's section
            self.fields['workingcode'].queryset = WorkingCode.objects.filter(
                                        section = instance.workingcode.section).order_by('section','name')
        else:
            # show all working code under department
            self.fields['workingcode'].queryset = WorkingCode.objects.filter(
                                        section__department = department).order_by('section','name')
        # self.fields['client'].queryset = Client.objects.filter(company=company)
        # print(kwargs)

    class Meta:
        model = Working
        fields = ['user','working_date','workingcode','note']
        # exclude = ['name']

class WorkingAdmin(admin.ModelAdmin):
    search_fields = ['user__username','user__first_name','user__last_name','user__en','note']
    list_filter = [WorkingDateListFilter,SectionListFilter,'status']
    list_display = ('user',get_en,get_section,'working_date','workingcode',status_colored,'status')
    # list_editable = ('get_color')
    readonly_fields = ['status','created_date','modified_date','approved_date',
                        'accepted_date','accepted_result','completed_date','completed']
    form = WorkingForm

    fieldsets = [
        ('Basic Information',{'fields': ['user',('working_date','workingcode'),
                                    'note','status','created_date','modified_date']}),
        ('Approval Flow Information',{'fields': ['approved_date',('accepted_date','accepted_result'),('completed_date','completed')]}),

    ]
    # def get_form(self, request, **kwargs):
    #     form = super(WorkingAdmin, self).get_form(request, **kwargs)
    #     form.current_user = request.user
    #     return form
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        # print (request.user)
        return form

    # Show only working under Department
    def get_queryset(self,request):
        
        # qs = super(WorkingAdmin, self).get_queryset(request)
        qs = super().get_queryset(request)
        # print (request.user)
        self.request = request

        if not request.user.is_superuser :
            department = request.user.section.department
            qs = qs.filter(user__section__department = department).order_by('-working_date')
        # print ('Department = %s' % department)
        return qs

    def clean_workingcode(self):
        # do something that validates your data
        # print ('On clean_workingcode')
        return self.cleaned_data['workingcode']

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     super().save_model(request, obj, form, change)

    

admin.site.register(Working,WorkingAdmin)
