from django.shortcuts import render

# Create your views here.

from django.views.generic import DetailView,CreateView,UpdateView,DeleteView,ListView

from .models import Company

class CompanyListView(ListView):
	model = Company

class CompanyDetailView(DetailView):
	model = Company
