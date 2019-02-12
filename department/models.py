from django.db import models

# Create your models here.
class Department(models.Model):
	name 				= models.CharField(primary_key=True,max_length=50,null = False)
	description 		= models.TextField(null = True,blank = True)

	def __str__(self):
		return ('%s' % (self.name))


class Section(models.Model):
	name 				= models.CharField(primary_key=True,max_length=50,null = False)
	department 			= models.ForeignKey(Department,
								blank=True,null=True,
								on_delete=models.CASCADE,
								related_name = 'sections')
	description 		= models.TextField(null = True,blank = True)

	def __str__(self):
		return ('%s (%s)' % (self.name,self.department))