from rest_framework import serializers
from django.contrib.auth.models import User,Group,Permission
from .models import UserRoles,Role,User

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


class CreateRoleSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Role
        fields = '__all__'

