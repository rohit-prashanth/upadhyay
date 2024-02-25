from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


# Create your views here.
class Userlogin(View):
    def get(self,request):
        return HttpResponse("Hi, You are in Login page..!!")