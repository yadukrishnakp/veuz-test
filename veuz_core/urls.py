"""root_project_django_v4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve
from veuz_core.views import page_not_found_view, custom_500

admin.site.site_header = "Veuz"
admin.site.site_title = "Veuz"

schema_view = get_schema_view(
   openapi.Info(
      title="Veuz",
      default_version='v1',
      terms_of_service="",
      contact=openapi.Contact(email="yadu@aventusinformatics.com"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    
    
    path('admin/', admin.site.urls),
    
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^assets/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),


    path('', include('apps.home.urls')),
    path('users/', include('apps.users.urls')),
    path('auth/', include('apps.authentication.urls')),
    path('admins/', include('apps.admins.urls')),
    path('employee/', include('apps.employee.urls')),    
    
    
    re_path(r'^api/', include([
        
        path('auth/', include('apps.authentication.api.urls')),
        path('users/', include('apps.users.api.urls')),
        path('home/', include('apps.home.api.urls')),
        path('employee/', include('apps.employee.api.urls')),
    
        re_path(r'^docs/', include([

            path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
            path("redoc", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        ])),    
    ])),    
    
        
    
] 


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found_view
handler500 = custom_500
