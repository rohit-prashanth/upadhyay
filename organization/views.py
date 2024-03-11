from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import OrganizationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group,Permission
from rest_framework import viewsets, status
from .models import Organization
from django.contrib.auth.mixins import PermissionRequiredMixin,AccessMixin,LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required


class Organization(PermissionRequiredMixin,GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    permission_required = ['organization.add_organization','organization.view_organization']
    permission_denied_message = {"details":"UnAuthorised"}
    raise_exception = False
    login_url = '/permission-denial/'
    serializer_class = OrganizationSerializer

    def get(self,request):
        try:
            org = Organization.objects.all()
            serializer = OrganizationSerializer(org,many=True)

            return Response(serializer.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))


    def post(self,request):
        try:
            data = request.data
            serializer = OrganizationSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)

        except Exception as e:
            return Response(str(e))