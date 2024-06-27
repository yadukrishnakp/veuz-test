from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'employee'

urlpatterns = [
    path('', login_required(views.EmployeeManagementView.as_view()), name='employee_management.index'),
    path('create/', login_required(views.EmployeeManagementCreateOrUpdateView.as_view()), name='employee_management.create'),
    path('<str:id>/update/', views.EmployeeManagementCreateOrUpdateView.as_view(), name='employee_management.update'),
    path('employee-management-datatable', login_required(views.LoadEmployeeManagementDatatable.as_view()), name='load.employee_management.datatable'),
    path('destroy_records/', login_required(views.DestroyEmployeeManagementRecordsView.as_view()), name='employee_management.records.destroy'),
    path('active-or-inactive/', login_required(views.EmployeeManagementStatusChange.as_view()), name="employee_management.status_change"),

    path('<str:id>/update-settings/', views.SettingsManagementCreateOrUpdateView.as_view(), name='employee_settings_management.update'),
    path('settings-create/', login_required(views.SettingsManagementCreateOrUpdateView.as_view()), name='employee_settings_management.create'),
]