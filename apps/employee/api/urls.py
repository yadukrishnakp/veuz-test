from django.urls import path
from . import views

urlpatterns = [      
   path('create-or-update-employee',views.CreateorUpdateEmployeeApiView.as_view()),
   path('get-employee-list',views.GetEmployeeDetailsOrListApiView.as_view()),
   path('delete-employee',views.DeleteEmployeeAPIView.as_view()),
]