from rest_framework import serializers
from apps.employee.models import EmployeeDetails


class EmployeeDetailsOrListingSchema(serializers.ModelSerializer):
    class Meta:
        model  = EmployeeDetails
        fields = ['id', 'slug', 'name', 'email', 'phonenumber']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas