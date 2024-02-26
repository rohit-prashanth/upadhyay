from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


# Create your views here.
class Userlogin(View):
    def get(self,request):
        return HttpResponse("Hi, You are in Login page..!!")

    def post(self,request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return 'Sucessfully logged In'
        else:
            return 'Invalid Username or Password'
