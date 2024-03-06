from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer,GroupPermissionsSerializer,UserPermissionsSerializer,UserRoleSerializer,RoleMasterSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group,Permission
from rest_framework import viewsets, status
from .models import UserRoles,Role
from django.contrib.auth.mixins import PermissionRequiredMixin


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


class Userlogout(APIView):
    def post(self,request):
        logout(request)
        return {'status': False}
        


class UserCreate(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    
    def get(self,request):
        user = User.objects.first()
        # all_fields = user._meta.get_fields()

        # print(all_fields)
        serializers = UserSerializer(user)
        return Response({"fields":serializers.data})


    def post(self,request):
        try:
            data = request.data

            serializers = UserSerializer(data=data)

            if serializers.is_valid():
                serializers.save()    
                return Response(serializers.data)
            else:
                return Response(serializers.errors)
        
        except Exception as e:
             return Response(str(e))
        

class GroupPermissionsClass(PermissionRequiredMixin,APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = ['Group.add_group','Group.view_group','Group.change_group','Group.delete_group']

    def get(self,request):
        try:
            group_list = Group.objects.all()

            serializers = GroupPermissionsSerializer(group_list, many=True)

            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))
     
    #  def post(self,request):
    #     data = request.data


class AssignGroup(APIView):

    def post(self,request):
        try:
            data = request.data
            print(data)
            if 'user_id' in data and 'group_ids' in data :
                print(data)
                user_id = data['user_id']
                print(user_id)
                group_ids = data['group_ids']
                user = User.objects.get(pk=user_id)
                print(user)
                # user.groups.remove(**group_ids)
                # user.groups.add(group_ids)
                for group in group_ids:
                    user.groups.add(group)
                serializer = UserSerializer(user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'required user_id field'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
        except Exception as e:
            return Response(str(e))

class UserPermissionsClass(APIView):
     
    def get(self,request):
          
        group_list = Permission.objects.all()

        serializers = UserPermissionsSerializer(group_list, many=True)

        return Response(serializers.data,status=status.HTTP_200_OK)


class UserRole(APIView):
     
    def get(self,request):
          
        role_list = UserRoles.objects.all()
        serializers = UserRoleSerializer(role_list, many=True)
        return Response(serializers.data,status=status.HTTP_200_OK)


    def post(self,request):
         
        data = request.data
        role = data['role']
        serializers = UserRoleSerializer(data=data)

        if serializers.is_valid():
            serializers.save()
            serializers.group.add(role)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializers.errors)
        

class RoleMaster(APIView):

     def get(self,request):
        roles =  Role.objects.all()

        serializers = RoleMasterSerializer(roles,many=True)

        return Response(serializers.data, status=status.HTTP_200_OK)

