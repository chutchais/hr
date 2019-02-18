from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.utils import timezone


from .models import User


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