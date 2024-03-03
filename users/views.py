from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class Userlogin(APIView):
    def get_tokens_for_user(self,user):
                    refresh = RefreshToken.for_user(user)
                    return {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
    

    def get(self,request):
        data = User.objects.all()
        serializer = UserSerializer(data,many=True) 
        return Response(serializer.data)

    def post(self,request):
        query_params = request.data
        if "userName" in query_params and "password" in query_params:
            username = query_params["userName"]
            password = query_params["password"]
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                token = self.get_tokens_for_user(user)
                return Response({'status' : True, 'token' : token})
            else:
                return Response({'status': False})
            
        else:
            return Response({'status': False})


class Userlogout(View):
    def post(self,request):
        logout(request)
        return {'status': False}
        