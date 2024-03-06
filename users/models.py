from django.db import models
from django.conf import settings
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class Role(models.Model):
	"""
	It consists of all available roles information
	"""
	name = models.CharField(max_length=250)
	code = models.CharField(max_length=50,unique=True)
	# user_roles = models.ManyToManyField(
	# 								User,
    #                                 through='UserRoles')
	# 								#related_name='user_roles')
	# 								#db_table='user_roles')
	is_active = models.BooleanField(default=True)
	# organization = models.ForeignKey('organization.Organization', 
	# 								related_name="role", 
	# 								null=True,
	# 								 on_delete=models.SET_NULL)
	date_created = models.DateTimeField(auto_now_add=True)
	date_last_modified = models.DateTimeField(null=True,auto_now=True)
	created_by = models.ForeignKey(User, 
									related_name="user_created", 
									null=True,
								   on_delete=models.SET_NULL
								   )
	modified_by = models.ForeignKey(User, 
									related_name="user_modified", 
									null=True,
									on_delete=models.SET_NULL)
	groups = models.ManyToManyField(Group,
                                    related_name="user_group_permissions",
								    )

	class Meta:
		db_table = "role_master"

	def __str__(self):
		return self.name

class UserRoles(models.Model):
	role=models.ForeignKey(Role,on_delete=models.CASCADE,null=True,related_name='role_id')
	master=models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name='master_id')
	created_by_user = models.ForeignKey(User, 
									related_name="created_by_user", 
									null=True,
								   on_delete=models.SET_NULL)
	created_date = models.DateTimeField(auto_now_add=True,null=True)
	class Meta:
		db_table = "user_roles"
	
	def __str__(self):
		return self.master.username


class UserMaster(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    choice = (("Male","M"),
                ("Female","F"))
    gender = models.CharField(max_length=10,choices=choice,blank=True,null=True)
	


    def __str__(self):
	    return self.user.username

