from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer,GroupPermissionsSerializer,UserPermissionsSerializer,UserRoleSerializer,CreateRoleSerializer,RoleListSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group,Permission
from rest_framework import viewsets, status
from .models import UserRoles,Role
from django.contrib.auth.mixins import PermissionRequiredMixin,AccessMixin,LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from organization.models import Organization


class PermissionDenial(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        return Response({"status":"UnAuthorised"},status=status.HTTP_403_FORBIDDEN)


# Create your views here.
class Userlogin(APIView):

    def get_tokens_for_user(self,user):
                    refresh = RefreshToken.for_user(user)
                    return {
                                'refresh': str(refresh),
                                'access': str(refresh.access_token),
                            }
    

    def get(self,request):
        # data = User.objects.all()
        # serializer = UserSerializer(data,many=True) 
        # return Response(serializer.data)
        return Response({"status":"Not Found"},status=status.HTTP_404_NOT_FOUND)

    def post(self,request):
        try:
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
        
        except Exception as e:
             return Response(str(e))

class Userlogout(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            logout(request)
            return Response({'status': True})
        except Exception as e:
             return Response(str(e))

        


class UserCreate(PermissionRequiredMixin,GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = ['User.add_user']
    permission_denied_message = {"details":"UnAuthorised"}
    raise_exception = False
    login_url = '/permission-denial/'
    serializer_class = UserSerializer
    
    
    def get(self,request):
        try:
            user = User.objects.all()
            # all_fields = user._meta.get_fields()

            # print(all_fields)
            serializers = self.get_serializer(user,many=True)
            return Response({"fields":serializers.data})
        except Exception as e:
             return Response(str(e))


    def post(self,request):
        try:
            data = request.data

            serializers = self.get_serializer(data=data)

            if serializers.is_valid():
                serializers.save()    
                return Response(serializers.data)
            else:
                return Response(serializers.errors)
        
        except Exception as e:
             return Response(str(e))
        

class GroupPermissionsClass(PermissionRequiredMixin,GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = "auth.view_group"
    raise_exception = False
    login_url = '/permission-denial/'
    serializer_class = GroupPermissionsSerializer
    

    def get(self,request):
        try:
            print(request.user.is_authenticated)
            group_list = Group.objects.all()

            serializers = self.get_serializer(group_list, many=True)

            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))
     
    #  def post(self,request):
    #     data = request.data


class AssignRole(PermissionRequiredMixin,GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = ["auth.view_group","auth.change_user"]
    raise_exception = False
    login_url = '/permission-denial/'
    serializer_class = UserSerializer

    def post(self,request):
        try:
            data = request.data
            print(data)
            if 'user_id' in data and 'role_id' in data :
                print(data)
                user_id = data['user_id']
                print(user_id)
                group_ids = data['role_id']
                user = User.objects.get(pk=user_id)
                print(user)
                # user.groups.remove(**group_ids)
                # user.groups.add(group_ids)
                for group in group_ids:
                    user.groups.add(group)
                serializer = self.get_serializer(user)
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            else:
                return Response({'status': 'required user_id field'},status=status.HTTP_406_NOT_ACCEPTABLE)
            
        except Exception as e:
            return Response(str(e))

class UserPermissionsClass(PermissionRequiredMixin,GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = ["auth.view_permission","auth.add_permission","auth.change_permission"]
    raise_exception = False
    login_url = '/permission-denial/'
    serializer_class = UserPermissionsSerializer

    def get(self,request):
        try:
            group_list = Permission.objects.all()
            serializers = self.get_serializer(group_list, many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e))


class CreateRole(PermissionRequiredMixin,GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = ["users.view_userrole","users.add_userrole"]
    #,"users.add_userroles","users.change_userroles"
    raise_exception = False
    login_url = '/permission-denial/'
    serializer_class = CreateRoleSerializer

    def get(self,request):
        try:
            print(request.user.id)
            
            role = Role.objects.all()
            if role:
                serializers = RoleListSerializer(role,many=True)
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response({"status":False},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(str(e))

    def post(self,request):
        try: 
            data = request.data
            # org_id = data.pop("organization")
            user = self.request.user
            print(user)
            # org = Organization.objects.get(pk=org_id)
            # data["organization"] = org
            # data['created_by'] = user_id
            # data['modified_by'] = user_id
            print(data)

            serializers = self.get_serializer(data=data)

            if serializers.is_valid():
                serializers.save(created_by=user,modified_by=user)
                return Response(serializers.data,status=status.HTTP_201_CREATED)
            else:
                return Response(serializers.errors)
        
        except Exception as e:
            return Response(str(e))



