from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import UserMaster,Role,UserRoles


admin.site.register(UserMaster,UserAdmin)
admin.site.register(Role)
admin.site.register(UserRoles)



# @admin.register(UserMaster)
# class UniversalAdmin(admin.ModelAdmin):
#     def get_list_display(self, request):
#         return [field.name for field in self.model._meta.concrete_fields]