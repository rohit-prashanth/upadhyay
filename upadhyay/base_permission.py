from rest_framework.permissions import DjangoModelPermissions

class BaseModelPerm(DjangoModelPermissions):

    def get_custom_perms(self, method, view):
          app_name = view.model._meta.app_label
          print("\napp_name: ",app_name)
          print("method: ",method)
          cust_perms = [app_name+"."+perms for perms in view.extra_perms_map.get(method, [])]
          print("\ncust_perms: ",cust_perms)
          return cust_perms

    def has_permission(self, request, view):
       perms = self.get_required_permissions(request.method, view.model)
       print("\nperms: ",perms)
       perms.extend(self.get_custom_perms(request.method, view))
       print("\nextended_perms: ",perms)
       print("request.user: ",request.user)
       print("request.user.is_authenticated: ",request.user.is_authenticated)
       print("self.authenticated_users_only: ",self.authenticated_users_only)
       print("request.user.has_perms(perms): ",request.user.has_perms(perms))
       print("request.user.get_user_permissions: ", request.user.get_user_permissions())
       print("request.user.get_group_permissions: ",request.user.get_group_permissions())
       print("request.user.get_all_permissions: ",request.user.get_all_permissions())
       return (
          request.user and
          (request.user.is_authenticated or not self.authenticated_users_only) and
        request.user.has_perms(perms)
    )