from drf_yasg import openapi
import logging
from apps.users.models import Users
from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from veuz_core.helpers.custom_messages import _account_tem_suspended,_invalid_credentials
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
import json
from veuz_core.response import ResponseInfo
from apps.authentication.api.serializers import LoginSerializer, LogoutSerializer, RefreshTokenSerializer
from apps.authentication.api.schemas import LoginSchema
from veuz_core import settings
from veuz_core.helpers.helper import DataEncryption
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from veuz_core.helpers.custom_messages import _success
from veuz_core.helpers.custom_messages import _success

logger = logging.getLogger(__name__)
        

#Start Login 
class LoginAPIView(GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LoginAPIView, self).__init__(**kwargs)
        
    serializer_class = LoginSerializer
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)

            email    = serializer.validated_data.get('email', '')
            password = serializer.validated_data.get('password', '')
            try:
                user_instance = Users.objects.get(email=email)
            except:
                user_instance = None
            if user_instance:
                user = auth.authenticate(request=request, username=user_instance.email, password=password)
                
                if user:
                    serializer = LoginSchema(user, context={"request": request})
                    if not user.is_active:
                        data = {'user': {}, 'token': '', 'refresh': ''}
                        self.response_format['status_code'] = status.HTTP_202_ACCEPTED
                        self.response_format["data"] = data
                        self.response_format["status"] = False
                        self.response_format["message"] = _account_tem_suspended
                        return Response(self.response_format, status=status.HTTP_200_OK)
                    else:
                        final_out         = json.dumps(serializer.data)
                        key               = settings.E_COMMERCE_SECRET        
                        encrypted_data    = DataEncryption.encrypt(key, final_out)
                        access_tokens     = AccessToken.for_user(user)
                        refresh_token     = RefreshToken.for_user(user)             
                  
                        
                        data = {'user': encrypted_data, 'token': str(access_tokens), 'refresh': str(refresh_token)}
                        self.response_format['status_code'] = status.HTTP_200_OK
                        self.response_format["data"] = data
                        self.response_format["status"] = True
                        self.response_format["message"] = _success

                        return Response(self.response_format, status=status.HTTP_200_OK)

                else:
                    self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                    self.response_format["message"] = _invalid_credentials
                    self.response_format["status"] = False
                    return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

            else:
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = _invalid_credentials
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# End Login

class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
        
        
class RefreshTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshTokenSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RefreshTokenView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            refresh = RefreshToken.for_user(user)
            data = {'token': str(
                refresh.access_token), 'refresh': str(refresh)}
            self.response_format['status_code'] = 200
            self.response_format["data"] = data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            self.response_format['status_code'] = 101
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_200_OK)
        