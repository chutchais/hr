from django.contrib import admin

# Register your models here.
from .models import Attendance,AttendanceFile

# admin.site.register(Attendance)



class AttendanceFileAdmin(admin.ModelAdmin):
    search_fields = ['name','description']
    list_filter = []
    list_display = ('name','filename','description','uploaded','uploaded_date')
    # list_editable = ('color','start_time','end_time',)
    fieldsets = [
        ('Basic Information',{'fields': ['name','filename','description']}),
        ('Upload Information',{'fields': ['uploaded','uploaded_date']})
    ]
admin.site.register(AttendanceFile,AttendanceFileAdmin)


class AttendanceAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_filter = ['source','stamp_status']
    list_display = ('user','stamp_date','stamp_time','source','stamp_status')
    # list_editable = ('color','start_time','end_time',)
    fieldsets = [
        ('Basic Information',{'fields': ['user','attendancefile']}),
        ('Attendance Information',{'fields': ['stamp_date','stamp_time','source','stamp_status']})
    ]
admin.site.register(Attendance,AttendanceAdmin)

