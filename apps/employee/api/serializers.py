from rest_framework import serializers

from apps.employee.models import EmployeeDetails
from veuz_core.helpers.helper import get_token_user_or_none


class CreateOrUpdateEmployeeDetailsSerializer(serializers.ModelSerializer):
    employee_id   = serializers.IntegerField(required=False, allow_null=True)
    name          = serializers.CharField(required=True)
    email         = serializers.EmailField(required=True)
    phonenumber   = serializers.CharField(required=True)

    class Meta:
        model = EmployeeDetails
        fields = ['employee_id', 'name', 'email', 'phonenumber']

    def validate(self, attrs):
        employee_id = attrs.get('id', None)

        employee_query_set = EmployeeDetails.objects.exclude(pk=employee_id).filter(email=attrs['email'])

        if employee_query_set.exists():
            raise serializers.ValidationError({"employee_email": ('Employee Email already exists!')})
        return super().validate(attrs)

    def create(self, validated_data):
        request               = self.context.get('request',None)

        user_instance         = get_token_user_or_none(request)

        instance              = EmployeeDetails()
        instance.name         = validated_data.get('name',None)
        instance.email        = validated_data.get('email',None)
        instance.phonenumber  = validated_data.get('phonenumber',None)
        instance.created_by   = user_instance
        instance.modified_by  = user_instance
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        request               = self.context.get('request',None)

        instance.name         = validated_data.get('name',None)
        instance.email        = validated_data.get('email',None)
        instance.phonenumber  = validated_data.get('phonenumber',None)    
        instance.modified_by  = get_token_user_or_none(request)
        instance.save()
        return instance
    

class DeleteEmployeeSerializer(serializers.ModelSerializer): 
    id= serializers.ListField(child=serializers.IntegerField(), required=True)
   
    class Meta: 
        model   = EmployeeDetails
        fields  = ['id']