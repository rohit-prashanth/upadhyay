from django.db import models
from django.conf import settings
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# class RoleMaster(models.Model):
#     ROLE_CHOICES = (
#         (1, 'principal'),
#         (2, 'teacher'),
#         (3, 'frontdesk'),
#         (4, 'humanresource'),
#         (5, 'admin'),

#     )
#     role_id = models.PositiveSmallIntegerField(primary_key=True,blank=False, null=False)
#     role_name = models.CharField(max_length=50)

# class UserRoles(models.Model):
#     user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
#                                 on_delete=models.CASCADE)
#     ROLE_CHOICES = (
#         (1, 'principal'),
#         (2, 'teacher'),
#         (3, 'frontdesk'),
#         (4, 'humanresource'),
#         (5, 'admin'),

#     )
#     role_id = models.ForeignKey(RoleMaster,on_delete=models.CASCADE,choices=ROLE_CHOICES, blank=True, null=True)

class Role(models.Model):
	"""
	It consists of all available roles information
	"""
	name = models.CharField(max_length=250)
	code = models.CharField(max_length=50)
	user_roles = models.ManyToManyField(
									settings.AUTH_USER_MODEL,
                                    through='UserRoles')
									#related_name='user_roles')
									#db_table='user_roles')
	is_active = models.BooleanField(default=True)
	# organization = models.ForeignKey('organization.Organization', 
	# 								related_name="role", 
	# 								null=True,
	# 								 on_delete=models.SET_NULL)
	date_created = models.DateTimeField(default=timezone.now)
	date_last_modified = models.DateTimeField(null=True)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
									related_name="user_created", 
									null=True,
								   on_delete=models.SET_NULL)
	modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
									related_name="user_modified", 
									null=True,
									on_delete=models.SET_NULL)

	class Meta:
		db_table = "role_master"
		permissions = (
			("list_role", "list all Roles"),
		)

	def __str__(self):
		return self.name

class UserRoles(models.Model):
	role=models.ForeignKey(Role,on_delete=models.CASCADE,related_name='role_id')
	master=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='master_id')
	class Meta:
		db_table = "user_roles"
	
	def __str__(self):
		return self.master


class UserMaster(AbstractUser):
    choice = (("Male","M"),
                ("Female","F"))
    gender = models.CharField(max_length=10,choices=choice,blank=True,null=True) 

    class Meta:
        permissions = (
            ("list_user", "Can list User"),
            ("add_user", "Can add User"),
            ("change_user", "Can change User"),
            ("delete_user", "Can delete User"),
            ("manage_user", "Can manage user"),
        )



