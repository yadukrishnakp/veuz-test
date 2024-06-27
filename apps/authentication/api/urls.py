from django.urls import include, path, re_path
from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers

urlpatterns = [       
   re_path(r'^web/', include([
      path('login', views.LoginAPIView.as_view()),
      path('logout', views.LogoutAPIView.as_view()),
      path('refresh-token', views.RefreshTokenView.as_view()),
   ])),
]

