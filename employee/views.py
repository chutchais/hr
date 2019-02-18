from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from django.shortcuts import get_object_or_404
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone
import sys
import json

from .models import User
from company.models import Company
from department.models import Section



@api_view(['POST'])
@csrf_exempt
def upload(request):
	response_msg = ''
	if request.method=='POST':
		try :
			import datetime
			data = json.loads(request.body.decode("utf-8"))
			# Show all data
			for key in data:
				print (key,data[key])
			en 				= data['en']
			first_name 		= data['first_name']
			last_name 		= data['last_name']
			section			= data['section']
			company 		= data['company']
			username 		= data['username']
			# get company
			objCompany 		= Company.objects.get(name=company)
			# get section
			objSection 		= Section.objects.get(name=section)

			m = User.objects.create(username=username,en=en,first_name=first_name,last_name=last_name,
									section=objSection,company=objCompany)

			response_msg={'msg':'successful',
							'successful':True,
							'user': username}
		except OSError as err:
			response_msg={'msg':"OS error: {0}".format(err),
							'created':False}
		except ValueError:
			response_msg={'msg':"Object of type 'type' is not JSON serializable",
							'created':False}

		except TypeError:
			response_msg={'msg':sys.exc_info()[0],
							'created':False}
		except:
			response_msg={'msg':sys.exc_info()[0],
							'created':False}

	return JsonResponse (response_msg)

@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


class UserListView(LoginRequiredMixin,ListView):
	model = User

class UserDetailView(LoginRequiredMixin,DetailView):
	model = User
	def get_context_data(self, **kwargs):
		context     = super().get_context_data(**kwargs)
		user 		= self.request.user
		# section 	= user.section
		# department 	= section.department
		# # print(user.groups.all())
		# year = self.request.GET.get('year', None)
		# month = self.request.GET.get('month', None)

		# display mode (mode=None --> show Working Code(default) , mode=Status -->show status mode)
		mode = self.request.GET.get('mode', None)
		report_date 	= timezone.now()
		context['now'] 	= report_date
		context['mode'] 	= mode
		return context