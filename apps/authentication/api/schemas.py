from django.contrib.auth.models import Permission
from rest_framework import serializers
from apps.users.models import Users


class GetUserGroupsSerializer(serializers.ModelSerializer):
    
    value    =  serializers.IntegerField(source='pk')
    label    =  serializers.CharField(source='name')
    class Meta:
        model  = Permission
        fields = ['value','label']

class LoginSchema(serializers.ModelSerializer):
    user_groups = serializers.SerializerMethodField('get_user_groups')
    class Meta:
        model = Users
        fields = ['id','email','is_active', 'user_groups']
        
    def get_user_groups(self, obj):
        return GetUserGroupsSerializer(obj.user_groups.all(), many=True).data
#-----------------------end here--------------------------


