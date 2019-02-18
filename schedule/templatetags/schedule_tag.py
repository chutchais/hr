from django import template
from datetime import timedelta
from django.db.models import Avg,Sum
import datetime
import calendar

register = template.Library()

import os

# @register.simple_tag

@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    updated.update(kwargs)
    return updated.urlencode()

@register.simple_tag
def working_in_sction(working_list, section, status):
	i=0
	for working in working_list:
		if working.user.section == section and working.status == status :
			i=i+1
	return i

@register.filter()
def range_days(date):
	try :
		number_of_day = calendar.monthrange(date.year,date.month)[1]
		return range(number_of_day)
	except:
		return range(1)

@register.simple_tag
def next_month(current):
	dt1 = current.replace(day=1)
	dt2 = dt1 + timedelta(days=31)
	dt3 = dt2.replace(day=1)
	return dt3

@register.simple_tag
def add_month(current,num=1):
	dt1 = current.replace(day=1)
	dt2 = dt1 + timedelta(days=num*31)
	dt3 = dt2.replace(day=1)
	return dt3

@register.simple_tag
def sub_month(current,num):
	dt1 = current.replace(day=1)
	dt2 = dt1 - timedelta(days=num*25)
	dt3 = dt2.replace(day=1)
	return dt3

@register.simple_tag
def previous_month(current):
	dt1 = current.replace(day=1)
	dt2 = dt1 - timedelta(days=1)
	dt3 = dt2.replace(day=1)
	return dt3


@register.simple_tag
def get_working(working_list,user,year,month,day):
	for working in working_list:
		# if working.user == user and working.working_date.day == day :
		if working.user == user and working.working_date.year == year and working.working_date.month == month and working.working_date.day == day :
			return working

@register.simple_tag
def queryset_to_list(queryset):
	return list(queryset)
	
# @register.assignment_tag
# def original_container(obj,stowage):
# 	return obj.filter(original_stowage=stowage).first()
