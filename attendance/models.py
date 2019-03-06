from django.db import models
from django.db.models.signals import pre_save,post_save


from employee.models import User
# Create your models here.


class AttendanceFile(models.Model):
	name 			= models.CharField(max_length=100,blank=True, null=True)
	filename 		= models.FileField(upload_to='logs/attendances/%Y/%m/%d/',blank=True, null=True)
	description 	= models.CharField(max_length=255,blank=True, null=True)
	created_date 	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	uploaded		= models.BooleanField(default=False)
	uploaded_date	= models.DateTimeField(blank=True, null=True)

	def __str__(self):
		return ('%s' % (self.name))

	class Meta:
		permissions = (
			("import_attendance_file", "Can import attendances file"),
		)

	def get_absolute_url(self):
		return reverse('attendances:detail', kwargs={'pk': self.pk})

def pre_save_AttendanceFile(sender, instance, *args, **kwargs):
	# print (instance.created_date.year)
	if instance.name == None:
		instance.name = instance.filename


pre_save.connect(pre_save_AttendanceFile, sender=AttendanceFile)




class Attendance(models.Model):
	user			= models.ForeignKey(User,
							on_delete=models.CASCADE,
							related_name = 'attendances')
	attendancefile 	= models.ForeignKey(AttendanceFile,
							on_delete=models.CASCADE,
							related_name = 'attendances')
	stamp_date		= models.DateField()
	stamp_time		= models.TimeField()
	stamp_status	= models.CharField(max_length=5,null = True,blank = True)
	source		 	= models.CharField(max_length=10,null = True,blank = True)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)

	def __str__(self):
		return ('%s' % (self.user))

	class Meta:
		permissions = (
			("process_attendance_file", "Can process attendances file"),
		)

	def get_absolute_url(self):
		return reverse('attendances:detail', kwargs={'pk': self.pk})
