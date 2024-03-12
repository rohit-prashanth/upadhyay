from rest_framework import serializers
from django.contrib.auth.models import User,Group,Permission
from .models import UserRoles,Role,User
from organization.models import Organization

class UserSerializer(serializers.ModelSerializer):

    # password = serializers.CharField(
    #     style={'input_type': 'password'},
    #     write_only=True, allow_null=True, allow_blank=True
    # )
    class Meta:
        model = User
        fields = '__all__'

    
    def create(self,validated_data):
        data = validated_data
        password = str(data.pop("password"))
        data['username'] = data['username'].lower()
        user = User.objects.create(**data)
        user.set_password(password)
        user.save()

        # # By default user set to participant role
        # role = Role.objects.get(code=settings.PRT)
        # UserRoles.objects.create(id=generate_pk(),role=role,master=user)
        # # role.user_roles.add(user)
        return user
    

class GroupPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'



class UserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'



class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRoles
        fields = '__all__'

class RoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class CreateRoleSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=True, max_length=100)
    # code = serializers.CharField(required=True, max_length=100)
    # organization = serializers.IntegerField(required=True,min_value=0)
    # groups = serializers.ListField(
    #             child=serializers.IntegerField(min_value=0,required=True)
    #             )

    # def get_organization(self,value):
    #     try:
    #         print("value: ",value, type(value))
    #         org = Organization.objects.get(pk=value)
    #         return org
    #     except Exception as e:  
    #         return str(e)
    class Meta:
        model = Role
        fields = ['name','code','organization','groups']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print("Validated_data: ", validated_data)
        group_ids = validated_data.pop('groups')
        role = Role.objects.create(**validated_data)
        for group in group_ids:
            print( "adding group:", group)
            role.groups.add(group)
            
        print( "returning role:", role)
        return role 
        
        