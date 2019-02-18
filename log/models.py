
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from employee.models import User
# Create your models here.
class Log(models.Model):
	# ADD 		= 'ADD'
	# START		=  'STR'
	# CHANGE 		= 'CHG'
	# APPROVE		= 'APP'
	# PRE_APPROVE	= 'PRE'
	# ACCEPT		= 'ACC'
	# REJECT		= 'REJ'
	# LOG_TYPES = (
	# 	(ADD, 'Add'),
	# 	(START, 'Start Process'),
	# 	(CHANGE, 'Change'),
	# 	(APPROVE, 'Approve'),
	# 	(PRE_APPROVE, 'Pre-Approve'),
	# 	(ACCEPT, 'Accept'),
	# 	(REJECT,'Reject')
	# )

	WORKING 	=	'WORKING'
	FINISH 		= 	'FINISH'
	PRE_APPROVE =	'PRE_APPROVE'
	APPROVE   	= 	'APPROVE'
	ACKNOWLEDGE	= 	'ACKNOWLEDGE'
	ACCEPT 		= 	'ACCEPT'
	REJECT   	= 	'REJECT'
	COMPLETE 	= 	'COMPLETE'
	DRAFT 		= 	'DRAFT'
	START 		= 	'START'
	CHANGE 		= 	'CHANGE'


	STATUS_CHOICES = (
			(DRAFT 			, 'On Draft'),
			(START 			, 'Start process'),
			(PRE_APPROVE	, 'Pre-approv'),
			(APPROVE 		, 'Approv'),
			(ACKNOWLEDGE	, 'Acknowledge'),
			(ACCEPT 		, 'Accepted'),
			(REJECT 		, 'Rejected'),
			(COMPLETE 		, 'Completed'),
			(CHANGE 		, 'Change'),
		)

	note 			= models.TextField(null = True,blank = True)
	user 	 		= models.ForeignKey(User,on_delete=models.CASCADE,)
	log_type 		= models.CharField(max_length=20, choices=STATUS_CHOICES,default=DRAFT)
	created_date	= models.DateTimeField(auto_now_add=True)
	# ContentType
	content_type 	= models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id 		= models.PositiveIntegerField()
	content_object 	= GenericForeignKey('content_type', 'object_id')

	def __str__(self):
		return self.note