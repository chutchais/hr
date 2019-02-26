from django import template
from datetime import timedelta
from django.db.models import Avg,Sum,Count
import datetime
import calendar

register = template.Library()

import os

from schedule.models import Working

# @register.simple_tag

@register.simple_tag
def query_transform(request, **kwargs):
	updated = request.GET.copy()
	updated.update(kwargs)
	return updated.urlencode()

# @register.simple_tag
# def working_in_sction(working_list, section, status):
# 	i=0
# 	for working in working_list:
# 		if working.user.section == section and working.status == status :
# 			i=i+1
# 	return i

@register.simple_tag
def working_in_sction(qs_working, section, status):
	w = qs_working.filter(user__section=section,status=status)
	return w.count()

@register.simple_tag
def status_in_working(qs_working, section):
	w = qs_working.filter(user__section=section).values('status').annotate(Count('status'))
	# print (w)
	return w

@register.simple_tag
def user_in_working(qs_working, section):
	w = qs_working.filter(user__section=section).values('status').annotate(Count('status'))
	# print (w)
	return w

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
def is_holiday(year,month,day):
	d = datetime.date(int(year),int(month),int(day))
	day_str = d.strftime('%A')
	if day_str in ['Saturday','Sunday']:
		return True
	return False

	


# @register.simple_tag
# def get_working(working_list,user,year,month,day):
# 	for working in working_list:
# 		if working.user == user and working.working_date.year == year and working.working_date.month == month and working.working_date.day == day :
# 			return working

@register.simple_tag
def get_working_by_month(userid,year,month):
	try:
		d = datetime.date(int(year),int(month),1)
		w = Working.objects.filter(user__id = userid,
								working_date__year = year,
								working_date__month = month).values_list('working_date__day',flat=True)
		# print (w)
	except :
		# print ('%s -%s not found' % (user,day))
		w = None
	return w

@register.simple_tag
def get_workings(userid,year,month):
	try:
		w = Working.objects.filter(user__id = userid, working_date__year=year, working_date__month =month)
		# print (w)
	except :
		# print ('%s -%s not found' % (user,day))
		w = None
	return w 


@register.simple_tag
def get_working_month(qs_working,user,year,month):
	try:
		# w = qs_working.get(user=user, working_date__year=year,working_date__month =month)
		w = qs_working.filter(user = user,working_date__year=year,working_date__month =month).values_list('working_date__day',flat=True)
		# print (w)
	except :
		# print ('%s -%s not found' % (user,day))
		w = None
	return w 

@register.simple_tag
def get_working(user,year,month,day):
	# d= None
	try:
		d = datetime.date(int(year),int(month),int(day))
		w = Working.objects.select_related('workingcode').get(user=user, working_date = d)
	except :
		# print ('%s -%s -%s -%s not found' % (user,year,month,day))
		w = None
	return w
	# for working in working_list:
	# 	if working.user == user and working.working_date.year == year and working.working_date.month == month and working.working_date.day == day :
	# 		return working




@register.simple_tag
def queryset_to_list(queryset):
	return list(queryset)
	
# @register.assignment_tag
# def original_container(obj,stowage):
# 	return obj.filter(original_stowage=stowage).first()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
