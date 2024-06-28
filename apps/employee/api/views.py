from rest_framework import status, generics
from apps.employee.api.schemas import EmployeeDetailsOrListingSchema
from apps.employee.api.serializers import CreateOrUpdateEmployeeDetailsSerializer, DeleteEmployeeSerializer
from apps.employee.models import EmployeeDetails
from drf_yasg import openapi
from apps.users.models import Users
from veuz_core.helpers.helper import get_object_or_none
from veuz_core.helpers.response import ResponseInfo
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from veuz_core.helpers.pagination import RestPagination
from veuz_core.helpers.custom_messages import _success
import os, sys
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
# Create your views here.


class CreateorUpdateEmployeeApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateorUpdateEmployeeApiView, self).__init__(**kwargs)
    
    serializer_class          = CreateOrUpdateEmployeeDetailsSerializer
    # permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Employee"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data, context = {'request' : request})

            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            employee_instance = get_object_or_none(EmployeeDetails, pk=serializer.validated_data.get('employee_id', None))

            serializer = self.serializer_class(employee_instance, data=request.data, context = {'request' : request})
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
                
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetEmployeeDetailsOrListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetEmployeeDetailsOrListApiView, self).__init__(**kwargs)
    
    serializer_class    = EmployeeDetailsOrListingSchema
    permission_classes  = [IsAuthenticated]
    pagination_class    = RestPagination
  
    id        = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Enter The Id ", required=False)
  
    @swagger_auto_schema(tags=["Employee"], manual_parameters=[id], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            id    = request.GET.get('id', None)

            filter_set = Q()

            if id not in ['', None]:
                filter_set &= Q(id=id)

            user_instance = get_object_or_none(Users, pk=request.user.id)

            if not user_instance.is_superuser:
                filter_set &= Q(created_by_id=request.user.id)

            queryset = EmployeeDetails.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

class DeleteEmployeeAPIView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteEmployeeAPIView, self).__init__(**kwargs)

    serializer_class    = DeleteEmployeeSerializer
    permission_classes  = (IsAuthenticated,)

    @swagger_auto_schema(tags   = ["Employee"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',None)
            EmployeeDetails.objects.filter(id__in = ids).delete()

            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e: 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 