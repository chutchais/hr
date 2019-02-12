from django.db import models

# Create your models here.
from employee.models import Employee

class Overtime(models.Model):
	overtime_id 		= models.AutoField(primary_key=True)
	name 				= models.CharField(max_length=50,null = False)
	description 		= models.TextField(null = True,blank = True)
	created_date		= models.DateTimeField(auto_now_add=True)
	created_by			= models.CharField(max_length=50,null = False)
	draft				= models.BooleanField(default=True)
	approved_date		= models.DateTimeField(blank=True, null=True)
	approved_by			= models.CharField(max_length=50,null = False)
	received_date		= models.DateTimeField(blank=True, null=True)
	received_by			= models.CharField(max_length=50,null = False)

	def __str__(self):
		return ('%s' % (self.name))

class OvertimeItem(models.Model):
	item_id 		= models.AutoField(primary_key=True)
	overtime  		= models.ForeignKey(Overtime,
								blank=True,null=True,on_delete=models.CASCADE,
								related_name = 'overtimes')
	employee  		= models.ForeignKey(Employee,
								blank=True,null=True,on_delete=models.CASCADE,
								related_name = 'overtimes')
	time1_start		= models.TimeField()
	time1_stop		= models.TimeField()
	time1_total		= models.FloatField(default=0)
	time1_remark	= models.TextField()
	time2_start		= models.TimeField()
	time2_stop		= models.TimeField()
	time2_rate10	= models.FloatField(default=0)
	time2_rate15	= models.FloatField(default=0)
	time2_rate20	= models.FloatField(default=0)
	time2_total		= models.FloatField(default=0)
	time2_additional= models.FloatField(default=0)
	time2_remark	= models.TextField()
	canceled		= models.BooleanField(default=False)
	reason			= models.TextField()
	
	def __str__(self):
		return ('%s' % (self.employee))