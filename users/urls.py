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

urlpatterns = [
    
    path('permission-denial/', views.PermissionDenial.as_view(), name= 'permission-denial'),
    path('login/', views.Userlogin.as_view(), name= 'userlogin'),
    path('logout/', views.Userlogout.as_view(), name= 'userlogout'),
    path('view-user/', views.ViewUser.as_view(), name= 'view-user'),
    path('create-user/', views.UserCreate.as_view(), name= 'create-user'),    
    path('view-group-permissions/',views.GroupPermissionsClass.as_view(), name= 'view-group-permissions'),
    path('create-group-permissions/',views.CreateGroupPermissions.as_view(), name= 'create-group-permissions'),
    path('view-user-permissions/',views.UserPermissionsClass.as_view(), name= 'view-user-permissions'),
    # path('create-user-permissions/',views.CreateUserPermissions.as_view(), name= 'create-user-permissions'),
    path('view-roles/',views.ViewRoles.as_view(), name= 'view-role'),
    path('role/',views.CreateRole.as_view(), name= 'create-role'),
    # path('role-master/',views.RoleMaster.as_view(), name= 'role-master'),
    path('view-user-role/',views.ViewUserRole.as_view(), name= 'view-user-role'),
    path('assign-user-role/',views.AssignUserRole.as_view(), name= 'assign-user-role'),




]
