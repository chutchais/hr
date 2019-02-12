from django.db import models

# Create your models here.
class Company(models.Model):
	name 			= models.CharField(primary_key=True,max_length=50,null = False)
	description 	= models.TextField(null = True,blank = True)

	def __str__(self):
		return ('%s' % (self.name))