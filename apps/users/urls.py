from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include, re_path
from . import views


app_name = 'users'


urlpatterns = [
    

  re_path(r'^roles/', include([
        
        path('',login_required(views.RoleView.as_view()), name='roles.index'),
        path('load-roles-datatable',views.LoadRolesDatatable.as_view(), name='load.roles.datatable'),
        path('create', login_required(views.RolesCreateOrUpdateView.as_view()), name='roles.create'),
        path('destroy/', views.DestroyRolesView.as_view(), name='roles.records.destroy'),
        path('<str:id>/update/',login_required(views.RolesCreateOrUpdateView.as_view()), name='roles.update'),
        path('generate-permission-tree',views.GeneratePermissionInTreeView.as_view(), name='generate.permission.tree'),
        path('check-role/',login_required(views.CheckRoleNameExistRecordsView.as_view()),name='admin.role_name_exist_check'),
        path('check-group/',login_required(views.CheckGroupNameExistRecordsView.as_view()),name='admin.group_name_exist_check'),

    ])),

    # Group based views url
    re_path(r'^groups/', include([
        path('',login_required(views.GroupView.as_view()), name='groups.index'),
        path('load-groups-datatable',views.LoadGroupDatatable.as_view(), name='load.groups.datatable'),
        path('destroy/', views.DestroyGroupView.as_view(), name='groups.records.destroy'),
        path('create', login_required(views.CreateOrUpdateGroupView.as_view()), name='groups.create'),
        path('<str:id>/update/',login_required(views.CreateOrUpdateGroupView.as_view()), name='update-groups'),
    ])),
    
    re_path(r'^customer/', include([
        path('',views.CustomerView.as_view(), name='customers.index'),
        path('load-customer-datatable',views.LoadCustomerDatatable.as_view(), name='load.customers.datatable'),
    ])),
    
    
    
]
