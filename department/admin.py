from django.contrib import admin

# Register your models here.
from department.models import Department,Section


class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description')
    fieldsets = [
        ('Basic Information',{'fields': ['name','description']}),
    ]
admin.site.register(Department,DepartmentAdmin)


class SectionAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = ['department']
    list_display = ('name','department','description')
    fieldsets = [
        ('Basic Information',{'fields': ['name','department','description']}),
    ]
admin.site.register(Section,SectionAdmin)