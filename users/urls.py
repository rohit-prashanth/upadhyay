"""
URL configuration for upadhyay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('permission-denial/', views.PermissionDenial.as_view(), name= 'permission-denial'),
    path('login/', views.Userlogin.as_view(), name= 'userlogin'),
    path('logout/', views.Userlogout.as_view(), name= 'userlogout'),
    path('create-user/', views.UserCreate.as_view(), name= 'create-user'),
    path('group-permissions/',views.GroupPermissionsClass.as_view(), name= 'group-permissions'),
    path('user-permissions/',views.UserPermissionsClass.as_view(), name= 'group-permissions'),
    path('create-role/',views.CreateRole.as_view(), name= 'create-role'),
    # path('role-master/',views.RoleMaster.as_view(), name= 'role-master'),
    path('assign-user-role/',views.AssignRole.as_view(), name= 'assign-user-role'),




]
