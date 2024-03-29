from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import (
    UserSerializer,GroupPermissionsSerializer,
    UserPermissionsSerializer,UserRoleSerializer,
    CreateRoleSerializer,RoleListSerializer,
    UserRoleListSerializer, UserViewSerializer,
    CreateGroupPermissionsSerializer,CreateUserPermissionsSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth.models import Group,Permission
from rest_framework import viewsets, status
from .models import UserRoles,Role
from django.contrib.auth.mixins import PermissionRequiredMixin,AccessMixin,LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from organization.models import Organization
from upadhyay.base_permission import BaseModelPerm


class PermissionDenial(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    '''    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,DjangoModelPermissions]
    permission_required = ['auth.add_user']
    permission_denied_message = {"details":"UnAuthorised"}
    raise_exception = False
    login_url = '/permission-denial/'
    serializer_class = UserSerializer

    queryset = User.objects.all()
    '''
    def get(self,request):
        return Response({"status":"UnAuthorised"},status=status.HTTP_403_FORBIDDEN)


# Create your views here.
class Userlogin(APIView):
    permission_classes = [AllowAny]


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
            print(query_params)
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

class ViewUser(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = User
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
    'GET': ["view_user"],
    }
    
    queryset = User.objects.all()
    def get(self,request):
        try:
            # meta = request.META
            token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
            print(request.user)
            user = User.objects.get(pk = request.user.id)
            serializer = self.get_serializer(user)
            print(token)
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e))
            




class UserCreate(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = User
    serializer_class = UserViewSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {}

    # 'GET': ["add_user"],
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,DjangoModelPermissions]
    # permission_required = ['auth.add_user']
    # permission_denied_message = {"details":"UnAuthorised"}
    # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = UserSerializer

    queryset = User.objects.all()
    
    # def get(self,request):
    #     try:
    #         user = User.objects.all()
    #         # all_fields = user._meta.get_fields()
    #         # print(all_fields)
    #         serializers = self.get_serializer(user,many=True)
    #         return Response({"fields":serializers.data})
    #     except Exception as e:
    #          return Response(str(e))


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
        

class GroupPermissionsClass(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = Group
    serializer_class = GroupPermissionsSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
    'GET': ["view_group"],
    }

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = "auth.view_group"
    # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = GroupPermissionsSerializer
    

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
        

class CreateGroupPermissions(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = Group
    serializer_class = CreateGroupPermissionsSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {}

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = ["auth.add_group","auth.change_group"]
    # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = CreateGroupPermissionsSerializer

    def post(self,request):
        try:
            data = request.data
            if "name" in data and "permissions" in data:
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response({"Status":"Missing Required Fields"},status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            return Response(str(e))

class ViewUserRole(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = UserRoles
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
        'GET': ["view_userroles"],
        }

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = ["auth.view_userroles"]
    # # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = UserRoleSerializer

    def get(self,request):
        try:
            userrole = UserRoles.objects.all()
            serializer = UserRoleListSerializer(userrole,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))

class AssignUserRole(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = UserRoles
    serializer_class = UserRoleSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
        
        }
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = ["auth.change_userroles","auth.add_userroles"]
    # # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = UserRoleSerializer

    # def get(self,request):
    #     try:
    #         userrole = UserRoles.objects.all()
    #         serializer = UserRoleListSerializer(userrole,many=True)

    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response(str(e))

    def post(self,request):
        try:
            data = request.data
            print(data)

            if 'master' in data and 'user' in data:
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(created_by_user=self.request.user)
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                    return Response({"Status":"Missing Required Fields"},status=status.HTTP_406_NOT_ACCEPTABLE)
            
        except Exception as e:
            return Response(str(e))

class UserPermissionsClass(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = Permission
    serializer_class = UserPermissionsSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
        'GET': ["view_permission"],
        }
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = ["auth.view_permission"]
    # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = UserPermissionsSerializer

    def get(self,request):
        try:
            group_list = Permission.objects.all()
            serializers = self.get_serializer(group_list, many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e))


class CreateUserPermissions(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = Permission
    serializer_class = CreateUserPermissionsSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
        
        }
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = ["auth.add_permission","auth.change_permission"]
    # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = CreateUserPermissionsSerializer


    def post(self,request):
        try:
            data = request.data
            if 'master' in data and 'user' in data:
                serializer = self.get_serializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save(created_by_user=self.request.user)
                    return Response(serializer.data,status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                    return Response({"Status":"Missing Required Fields"},status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response(str(e))


class ViewRoles(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = Role
    serializer_class = RoleListSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
        'GET': ["view_role"],
        }
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = ["users.view_role"]
    # #,"users.add_userroles","users.change_userroles"
    # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = RoleListSerializer

    def get(self,request):
        try:
            print(request.user.id)
            try:
                userrole = UserRoles.objects.get(master = request.user.id)
            except Exception as e:
                return Response({"status":False},status=status.HTTP_404_NOT_FOUND)
            role = self.get_queryset()
            userrole = role.filter(pk=userrole.role.id)
            print("\nuserrole: ",userrole,type(userrole))
            if userrole:
                serializers = self.get_serializer(userrole,many=True)
                return Response(serializers.data,status=status.HTTP_200_OK)
            return Response({"status":False},status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(str(e))

class CreateRole(GenericAPIView):
    authentication_classes = [JWTAuthentication]
    model = Role
    serializer_class = CreateRoleSerializer
    permission_classes = (IsAuthenticated,BaseModelPerm)
    queryset = model.objects.all()
    extra_perms_map = {
        
        }
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    # permission_required = ["users.add_role","users.change_role",]
    # raise_exception = False
    # login_url = '/permission-denial/'
    # serializer_class = CreateRoleSerializer

    # def get(self,request):
    #     try:
    #         print(request.user.id)
            
    #         role = Role.objects.all()
    #         if role:
    #             serializers = RoleListSerializer(role,many=True)
    #             return Response(serializers.data,status=status.HTTP_200_OK)
    #         return Response({"status":False},status=status.HTTP_404_NOT_FOUND)
        
    #     except Exception as e:
    #         return Response(str(e))

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



