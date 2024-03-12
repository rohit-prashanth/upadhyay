from rest_framework import serializers
from .models import Organization



class OrganizationSerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True, max_length=100)
    code = serializers.CharField(required=True, max_length=20)
    # user = serializers.IntegerField(required=False)

    class Meta:
        model = Organization
        fields = ['name','code']


    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print("Validated_data: ", validated_data)
        # validated_data['created_by'] = self.request.user.id
        # validate_data['modified_by'] = self.request.user.id
        
        return Organization.objects.create(**validated_data)



class OrganizationlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
