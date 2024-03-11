from django.db import models
from users.models import User

class Organization(models.Model):
    
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=50,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(null=True,auto_now=True)
    created_by = models.ForeignKey(User, 
									related_name="org_created_by", 
									null=True,
								   on_delete=models.SET_NULL
								   )
    modified_by = models.ForeignKey(User, 
									related_name="org_modified_by", 
									null=True,
									on_delete=models.SET_NULL)




    def __str__(self):
	    return self.name
