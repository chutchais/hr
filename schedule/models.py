from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
# from django.core.urlresolvers import reverse

from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from department.models import Section
from employee.models import User
from attendance.models import Attendance

from log.models import Log

# Create your models here.
class WorkingCode(models.Model):
	name 			= models.CharField(max_length=50,null = False)
	section 		= models.ForeignKey(Section,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'workingcodes')
	start_time 		= models.TimeField(null=True,blank=True)
	end_time 		= models.TimeField(null=True,blank=True)
	description 	= models.TextField(null = True,blank = True)
	color 			= ColorField(default='#CCFFFF')
	dayoff			= models.BooleanField(default=False)
	active			= models.BooleanField(default=True)
	logs 			= GenericRelation(Log,related_query_name='workingcodes')

	class Meta:
		unique_together = (('name','section'))

	def __str__(self):
		return ('%s %s (%s to %s)' % (self.name,self.section,self.start_time,self.end_time))

	def get_color_style(self):
		if self.color:
			return ('style="background-color:%s" class="text-center"' % self.color)

# Draft -- On progressing
# Pre-approve -- Waiting for pre Approve by Superintendent
# Approv -- Waiting for Approv by manager
# Acknoledge -- Waiting for HR payroll ack
# Accepted -- Accepted by PayRoll staff
# Rejected -- Rejected by PayRoll staff (need creater to modify)
# Completed -- Import to TigerSoft
WORKING 	=	'WORKING'
FINISH 		= 	'FINISH'
PRE_APPROVE =	'PRE_APPROVE'
APPROVE   	= 	'APPROVE'
ACKNOWLEDGE	= 	'ACKNOWLEDGE'
ACCEPT 		= 	'ACCEPT'
REJECT   	= 	'REJECT'
COMPLETE 	= 	'COMPLETE'
DRAFT 		= 	'DRAFT'


STATUS_CHOICES = (
		(DRAFT 			, 'On Draft'),
		(PRE_APPROVE	, 'Pre-approv'),
		(APPROVE 		, 'Approv'),
		(ACKNOWLEDGE	, 'Acknowledge'),
		(ACCEPT 		, 'Accepted'),
		(REJECT 		, 'Rejected'),
		(COMPLETE 		, 'Completed'),
	)


NA 			= 'NA'
ACCEPT_CHOICES = (
		(NA 			, 'Not Defined yet'),
		(ACCEPT 		, 'Accepted'),
		(REJECT 		, 'Rejected'),
	)

class Working(models.Model):
	user			= models.ForeignKey(User,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'workings')
	working_date	= models.DateField(null=True,blank=True)
	workingcode		= models.ForeignKey(WorkingCode,
							blank=True,null=True,
							on_delete=models.CASCADE,
							related_name = 'workings')
	note		 	= models.TextField(null = True,blank = True)
	status			= models.CharField(max_length=15,choices=STATUS_CHOICES,default=DRAFT)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	approved_date	= models.DateTimeField(blank=True, null=True)
	accepted_date	= models.DateTimeField(blank=True, null=True)
	accepted_result	= models.CharField(max_length=10,choices=ACCEPT_CHOICES,default=NA)
	completed 		= models.BooleanField(default=False)
	completed_date	= models.DateTimeField(blank=True, null=True)
	logs 			= GenericRelation(Log ,related_query_name='workings')

	class Meta:
		permissions = (
			("create_working", "Can create working schedule"),
			("pre_approve_working", "Can pre-approve working schedule"),
			("approve_working", "Can approve working schedule"),
			("accept_reject_working", "Can accept/reject working schedule"),
			("complete_working", "Can complete working schedule"),
		)
		unique_together = (('user','working_date'))

	def clean(self):
		# print ("On clean function..%s - %s" % (self.user.section,self.workingcode.section))
		# check logged user 's department must match with User's department
		print(self.user)
		if self.user.section != self.workingcode.section :
			raise ValidationError('Working Code: %s is not valid for section %s' % (self.workingcode,self.user.section))

	def save(self, *args, **kwargs):
		# do_something()
		print('Save to Log %s' % self._state.adding)
		# self.logs.create(note=self.note,user=self.user)
		super().save(*args, **kwargs)  # Call the "real" save() method.
		# save Log


	def __str__(self):
		return ('%s on %s' % (self.user,self.working_date))

	def get_working_style(self):
		if self.workingcode.color:
			return ('style="background-color:%s" class="text-center"' % self.workingcode.color)

	def get_status_style(self):
		if self.status == DRAFT :
			return ('badge badge-v')
		if self.status == APPROVE :
			return ('badge badge-primary')
		if self.status == PRE_APPROVE  :
			return ('badge badge-info')
		if self.status == ACKNOWLEDGE :
			return ('badge badge-warning')
		if self.status == ACCEPT :
			return ('badge badge-success')
		if self.status == REJECT :
			return ('badge badge-danger')
		if self.status == COMPLETE :
			return ('badge badge-secondary')
		return 'badge badge-light'

	def get_absolute_url(self):
		return reverse('schedule:detail', kwargs={'pk': self.pk})

	def get_attendance(self):
		from datetime import timedelta
		ta = Attendance.objects.filter(user=self.user,
										stamp_date__range = [self.working_date
										,self.working_date +  timedelta(days=1)]).order_by('stamp_date')
		return ta

