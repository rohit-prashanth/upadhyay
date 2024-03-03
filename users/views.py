from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


# Create your views here.
class Userlogin(APIView):
    def get(self,request):
        data = User.objects.all()
        serializer = UserSerializer(data,many=True) 
        return Response(serializer.data)

    def post(self,request):
        query_params = self.request.query_params.dict()
        return Response({'query_param': query_params})
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return {'status' : True}
        else:
            return {'status': False}


class Userlogout(View):
    def post(self,request):
        logout(request)
        return {'status': False}
        