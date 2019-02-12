from django.db import models
from django.core.exceptions import ValidationError
from colorfield.fields import ColorField
from department.models import Section
from employee.models import User

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

	class Meta:
		unique_together = (('name','section'))

	def __str__(self):
		return ('%s %s (%s to %s)' % (self.name,self.section,self.start_time,self.end_time))

	def get_color_style(self):
		if self.color:
			return ('style="background-color:%s" class="text-center"' % self.color)

# Working -- On progressing
# Pre-approve -- Approve by Superintendent
# Approved -- Approved by manager
# Accepted -- Accepted by PayRoll staff
# Rejected -- Rejected by PayRoll staff (need creater to modify)
# Completed -- Import to TigerSoft
WORKING 	=	'WORKING'
FINISH 		= 	'FINISH'
PRE_APPROVE =	'PRE_APPROVE'
APPROVE   	= 	'APPROVE'
ACCEPT 		= 	'ACCEPT'
REJECT   	= 	'REJECT'
COMPLETE 	= 	'COMPLETE'


STATUS_CHOICES = (
        (WORKING 		, 'On Working'),
        (FINISH 		, 'Finished'),
        (PRE_APPROVE	, 'Pre-approved'),
        (APPROVE 		, 'Approved'),
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
	status			= models.CharField(max_length=10,choices=STATUS_CHOICES,default=WORKING)
	created_date	= models.DateTimeField(auto_now_add=True)
	modified_date	= models.DateTimeField(blank=True, null=True,auto_now=True)
	approved_date	= models.DateTimeField(blank=True, null=True)
	accepted_date	= models.DateTimeField(blank=True, null=True)
	accepted_result	= models.CharField(max_length=10,choices=ACCEPT_CHOICES,default=NA)
	completed 		= models.BooleanField(default=False)
	completed_date	= models.DateTimeField(blank=True, null=True)

	class Meta:
		permissions = (
			("request_working", "Can request working schedule"),
			("approve_working", "Can approve working schedule"),
			("accept_working", "Can accept/reject working schedule"),
		)

	def clean(self):
		# print ("On clean function..%s - %s" % (self.user.section,self.workingcode.section))
		# check logged user 's department must match with User's department
		print(self.user)
		if self.user.section != self.workingcode.section :
			raise ValidationError('Working Code: %s is not valid for section %s' % (self.workingcode,self.user.section))

	def __str__(self):
		return ('%s on %s' % (self.user,self.working_date))

	def get_working_style(self):
		if self.workingcode.color:
			return ('style="background-color:%s" class="text-center"' % self.workingcode.color)

	def get_absolute_url(self):
		return reverse('schedule:detail', kwargs={'pk': self.pk})
