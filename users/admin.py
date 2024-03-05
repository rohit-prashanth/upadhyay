from django.contrib import admin

# Register your models here.
from .models import UserMaster


admin.site.register(UserMaster)

# @admin.register(UserMaster)
# class UniversalAdmin(admin.ModelAdmin):
#     def get_list_display(self, request):
#         return [field.name for field in self.model._meta.concrete_fields]