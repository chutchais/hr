from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
from company.models import Company
from department.models import Section

class Position(models.Model):
	name 				= models.CharField(primary_key=True,max_length=50,null = False)
	description 		= models.TextField(null = True,blank = True)

	def __str__(self):
		return ('%s' % (self.name))

# Techician
# Hastler
# Crane

ROLE_CHOICES = (
        ('Foreman', 'Foreman'),
        ('Leader', 'Leader'),
        ('Officer','Officer'),
        ('superintendent','superintendent'),
        ('Operator','Operator'),
        ('Manager','Manager')
    )

TITLE_CHOICES = (
        ('Mr', 'Mr.'),
        ('Ms', 'Ms.'),
        ('Mrs', 'Mrs.'),
        ('Miss','Miss.'),
    )
class User(AbstractUser):
	title				= models.CharField(max_length=10,choices=TITLE_CHOICES,default='Mr')
	en					= models.CharField(max_length=50,null = False)
	company 			= models.ForeignKey(Company,
								blank=True,null=True  ,on_delete=models.CASCADE,
								related_name = 'employees' )
	section				= models.ForeignKey(Section,
								blank=True,null=True , on_delete=models.CASCADE,
								related_name = 'employees')
	position 			= models.ForeignKey(Position,
								blank=True,null=True , on_delete=models.CASCADE,
								related_name = 'employees')
	description 		= models.TextField(null = True,blank = True)
	manager 			= models.ForeignKey('self', blank = True,null=True, related_name='employees',
								on_delete=models.SET_NULL)

	class Meta:
		unique_together = (('en','company'))

	def __str__(self):
		return ('%s %s' % (self.first_name,self.last_name))
