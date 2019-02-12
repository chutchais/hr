from django.contrib import admin

# Register your models here.
from company.models import Company

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','description')
    fieldsets = [
        ('Basic Information',{'fields': ['name','description']}),
    ]
admin.site.register(Company,CompanyAdmin)